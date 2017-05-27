import os
import json

import guitarpro
from guitarpro.base import NoteType, SlapEffect, PitchClass, SlideType

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page

# from basscloud.libs.lzstring import LZString


def instrument_type(track):
    if track.isPercussionTrack:
        return 'drums'
    id = track.channel.instrument
    if id in (0, 1, 2, 4, 5):
        return 'piano'
    if id > 31 and id < 40:
        return 'bass'

def encode_note(pitch):
    return str(pitch).replace('#', chr(9839)).replace('b', chr(9837))



class Track(object):
    name = ''

    def __init__(self):
        self.bars = {}
        self.extra_data = {}

    def add_sound(self, bar, beat, sound):
        ibar = bar.number
        if ibar not in  self.bars:
            self.bars[ibar] = {
                'bar': ibar,
                'sounds': []
            }
        self.bars[ibar]['sounds'].append(sound)

    def data(self):
        data = {
            'name': self.name,
            'bars': list(self.bars.values())
        }
        data.update(self.extra_data)
        return data


class PercussionTrack(Track):
    name = 'Percussions'

    def note_sound(self, beat, note):
        return {
            'code': note.value,
            'volume': note.velocity/100
        }

DRUMS = {
    44: ('hihat', ),
    35: ('kick', ),
    41: ('tom3', ),
    43: ('tom3', ), # Tom low
    45: ('tom2', ), # Tom medium
    38: ('snare', ),
    42: ('hihat', 0.5),
    46: ('hihat-open', 0.5),
    55: ('hihat-open', ),
    49: ('crash', 0.5),
    57: ('crash', ),
    47: ('tom1', ) # Tom high,
}
PERCUSSIONS = {
    39: ('clap', ),
    54: ('tambourine', 0.5),
    56: ('cowbell', ),
    60: ('bongo', ),
    61: ('conga', ), # should be bongo low
    63: ('bongo', ),
    61: ('conga', 0.75),

    69: ('cabasa', ),
    70: ('maracas', ),
    75: ('claves', )
}

BONGO_CONGA = {
    60: ('bongo',),
    61: ('conga',),
    62: ('conga',),
    63: ('conga',),
    64: ('conga',)
}

class PercussionMultiTrack(PercussionTrack):
    def __init__(self, name='Percussions'):
        self.tracks = {}

    def add_sound(self, bar, ibeat, sound):
        code = sound['code']
        if code in DRUMS:
            kit = 'drums'
            MAP = DRUMS
        elif code in PERCUSSIONS:
            kit = 'percussions'
            MAP = PERCUSSIONS
        elif code in BONGO_CONGA:
            kit = 'bongo'
            MAP = BONGO_CONGA
        else:
            print('Unsupported drum code: ', code)
            return

        sound['drum'] = MAP[code][0]
        if kit not in self.tracks:
            track = PercussionTrack()
            track.name = kit
            self.tracks[kit] = track
        else:
            track = self.tracks[kit]
        track.add_sound(bar, ibeat, sound)

    def data(self):
        return [track.data() for track in self.tracks.values()]


class StringTrack(Track):
    def __init__(self, track):
        super(StringTrack, self).__init__()
        self.track = track
        self.name = track.name
        
        strings_data = {
            string.number: {
                'name': str(string),
                'value': string.value
            } for string in track.strings
        }
        self.extra_data['strings'] = strings_data

    def note_sound(self, beat, note):
        pitch = PitchClass(note.realValue)
        pitch = encode_note(pitch)
        octave = divmod(note.realValue, 12)[0] - 1
        sound = {
            'volume': note.velocity/100,
            'note': {
                'name': pitch,
                'octave': octave,
                'length': beat.duration.value,
                'dotted': beat.duration.isDotted,
                'staccato': note.effect.staccato,
            }
        }
        return sound


class PianoTrack(StringTrack):
    def __init__(self, track):
        super(PianoTrack, self).__init__(track)

    def note_sound(self, beat, note):
        sound = super(PianoTrack, self).note_sound(beat, note)
        sound['string'] = '{0}{1}'.format(sound['note']['name'], sound['note']['octave'])
        if note.type == NoteType.tie:
            sound['prev'] = True
        return sound


class BassTrack(StringTrack):
    def __init__(self, track):
        super(BassTrack, self).__init__(track)
        self.stringsMap = {string.number: str(PitchClass(string.value)) for string in track.strings}

    def note_sound(self, beat, note):
        sound = super(BassTrack, self).note_sound(beat, note)
        sound.update({
            'string': self.stringsMap[note.string]
        })
        sound['note'].update({
            'fret': note.value
        })
        return sound


class Convertor(object):

    def __init__(self, f):
        self.song = guitarpro.parse(f)


    def convert(self):
        song = self.song
        # percussions_track = PercussionTrack()
        percussions_track = PercussionMultiTrack()
        tracks = [percussions_track]
        for track in song.tracks:
            instrument = instrument_type(track)
            if not instrument:
                continue

            if instrument == 'bass':
                instrument_track = BassTrack(track)
                tracks.append(instrument_track)
            elif instrument == 'piano':
                instrument_track = PianoTrack(track)
                tracks.append(instrument_track)
            else:
                instrument_track = percussions_track


            for bar in track.measures:
                barLength = bar.end - bar.start
                beatLength = barLength / bar.timeSignature.numerator
                for beat in bar.voices[0].beats:
                    beat.measure = bar
                    start = (beat.start - bar.start) / beatLength
                    for note in beat.notes:
                        sound = instrument_track.note_sound(beat, note)
                        ibeat = int(start) + 1
                        sound['beat'] = ibeat
                        sound['start'] = start - int(start)
                        instrument_track.add_sound(bar, ibeat, sound)

                break

            # bar_data = {
            #     'timeSignature': {
            #         'top': bar.timeSignature.numerator,
            #         'bottom': bar.timeSignature.denominator.value
            #     },
            #     'bpm': bar.tempo.value,
            # }

        return [track.data() for track in tracks]

@csrf_exempt
def upload(request):
    print(request.FILES)
    f = request.FILES['file']
    song = guitarpro.parse(f)

    return JsonResponse({})


@gzip_page
def get(request):
    filename = os.path.join(settings.MEDIA_ROOT, 'gp5', request.GET['file']+'.gp5')
    c = Convertor(filename)
    return JsonResponse({
        'tracks': c.convert()
    })