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


class Track(object):
    name = ''

    def __init__(self):
        self.bars = {}
        self.extra_data = {}

    def add_sound(self, bar, beat, note):
        ibar = bar.number
        if ibar not in  self.bars:
            self.bars[ibar] = {
                'bar': ibar,
                'sounds': []
            }
        sound = self.convert_note(beat, note)
        if sound:
            self.bars[ibar]['sounds'].append(sound)
        return sound

    def data(self):
        data = {
            'name': self.name,
            'bars': list(self.bars.values())
        }
        data.update(self.extra_data)
        return data


class PercussionTrack(Track):
    name = 'Percussions'

    def convert_note(self, beat, note):
        return {
            'code': note.value,
            'volume': note.velocity/100
        }


class PercussionMultiTrack(PercussionTrack):
    def __init__(self, name='Percussions'):
        self.tracks = {}

    def add_sound(self, bar, beat, note):
        code = note.value
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

        if kit not in self.tracks:
            track = PercussionTrack()
            track.name = kit
            self.tracks[kit] = track
        else:
            track = self.tracks[kit]
        sound = track.add_sound(bar, beat, note)
        value = MAP[code]
        sound['drum'] = value[0]
        if len(value) == 2:
            sound['volume'] = value[1]
        return sound

    def data(self):
        return [track.data() for track in self.tracks.values()]


class StringTrack(Track):
    def __init__(self, track):
        super(StringTrack, self).__init__()
        self.track = track
        self.name = track.name
        self._prevStringSound = {}
        self._prevStringNote = {}
        
        strings_data = {
            string.number: {
                'name': str(string),
                'value': string.value
            } for string in track.strings
        }
        self.extra_data['strings'] = strings_data

    def isTie(self, note):
        # note.type == NoteType.tie doesn't work in Python3
        return note.type.value == NoteType.tie.value

    def convert_note(self, beat, note):
        if self.isTie(note):
            # fix note value (maybe some bug in library)
            prevNote = self._prevStringNote.get(note.string)
            note.value = prevNote.value

        name = encode_note(PitchClass(note.realValue))
        octave = divmod(note.realValue, 12)[0] - 1
        sound = {
            'volume': note.velocity/100,
            'note': {
                'name': name,
                'octave': octave,
                'length': beat.duration.value,
                'dotted': beat.duration.isDotted,
                'staccato': note.effect.staccato,
            }
        }
        if self.isTie(note):
            sound['prev'] = True
            prevSound = self._prevStringSound.get(note.string)
            prevSound['next'] = True
            # print('TIE ', self.track.name, sound)
        return sound

    def add_sound(self, bar, beat, note):
        sound = super(StringTrack, self).add_sound(bar, beat, note)
        if sound:
            self._prevStringSound[note.string] = sound
            self._prevStringNote[note.string] = note
        return sound


class PianoTrack(StringTrack):
    def __init__(self, track):
        super(PianoTrack, self).__init__(track)

    def convert_note(self, beat, note):
        sound = super(PianoTrack, self).convert_note(beat, note)
        sound['string'] = '{0}{1}'.format(sound['note']['name'], sound['note']['octave'])

        return sound


class BassTrack(StringTrack):
    def __init__(self, track):
        super(BassTrack, self).__init__(track)
        self.stringsMap = {string.number: str(PitchClass(string.value)) for string in track.strings}
        self.pendingNotes = {}

    def isTie(self, note):
        # return (note.isTiedNote or note.type.value == NoteType.tie.value) and not note.effect.slides
        return (note.type.value == NoteType.tie.value) and not note.effect.slides

    def convert_note(self, beat, note):
        sound = super(BassTrack, self).convert_note(beat, note)

        style = 'finger'
        if beat.effect.isSlapEffect:
            style = {
                SlapEffect.slapping.value: 'slap',
                SlapEffect.popping.value: 'pop',
                SlapEffect.tapping.value: 'tap',
            } [beat.effect.slapEffect.value]
        if beat.effect.hasPickStroke:
            style = 'pick'

        if self.isTie(note):
            style = 'ring'

        noteType = {
            NoteType.normal.value: 'regular',
            NoteType.dead.value: 'ghost',
        }.get(note.type.value, 'regular')

        sound.update({
            'string': self.stringsMap[note.string],
            'style': style
        })

        if noteType == 'ghost':
            sound['note'] = {
                'type': 'ghost',
                'length': 16
            }
        else:
            sound['note'].update({
                'type': noteType,
                'fret': note.value
            })

        if note.string in self.pendingNotes:
            prevNote = self.pendingNotes[note.string]
            prevSound = prevNote.sound
            del self.pendingNotes[note.string]
            if prevNote.effect.hammer:
                prevSound['next'] = True
                sound['prev'] = True
                sound['style'] = 'hammer' if prevSound['note']['fret'] < sound['note']['fret'] else 'pull'
            else:
                # slide
                SLIDE_LENGTHS = {
                    4:  {'length': 4},
                    6:  {'length': 4, 'dotted': True},
                    8:  {'length': 8},
                    12: {'length': 8, 'dotted': True},
                    16: {'length': 16}
                }
                length = 1/(1/prevSound['note']['length'] + 1/sound['note']['length'])
                print(prevSound['note']['length'], length)
                if length in SLIDE_LENGTHS:
                    # join two notes into the one sound
                    prevSound['note'].update(SLIDE_LENGTHS[length])
                    prevSound['endNote'] = {key: sound['note'][key] for key in ('name', 'octave', 'fret')}
                    return # delete this note
                else:
                    print('let ring slide')
                    prevSound['note']['type'] = 'regular'
                    prevSound['next'] = True
                    sound['prev'] = True
                    sound['style'] = 'ring'
                    sound['note']['type'] = 'slide'
                    sound['note']['slide'] = {}
                    sound['endNote'] = {key: sound['note'][key] for key in ('name', 'octave', 'fret')}
                    sound['note'].update({key: prevSound['note'][key] for key in ('name', 'octave', 'fret')})
                    return sound

        if note.effect.hammer:
            note.sound = sound
            self.pendingNotes[note.string] = note

        if note.effect.slides:
            slide = note.effect.slides[0]
            sound['note']['type'] = 'slide'
            sound['note']['slide'] = {}
            if slide.value in (SlideType.outDownwards.value, SlideType.outUpwards.value, SlideType.intoFromBelow.value, SlideType.intoFromAbove.value):
                if slide.value in (SlideType.outDownwards.value, SlideType.intoFromBelow.value):
                    step = -1 * min(3, sound['note']['fret']-1)
                else:
                    step = min(3, 24-sound['note']['fret'])
                slideNoteVal = note.realValue + step
                slidePitch = PitchClass(slideNoteVal)
                slideNote = {
                    'name': encode_note(slidePitch),
                    'octave': divmod(slideNoteVal, 12)[0] - 1,
                    'fret': sound['note']['fret'] + step
                }
                sound['endNote'] = slideNote

                if slide.value in (SlideType.intoFromAbove.value, SlideType.intoFromBelow.value):
                    copy = slideNote.copy()
                    for attr in ('name', 'octave', 'fret'):
                        slideNote[attr] = sound['note'][attr]
                        sound['note'][attr] = copy[attr]
            else:
                # slide to the next note (process on next note)
                note.sound = sound
                self.pendingNotes[note.string] = note

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


            for bar in track.measures[:8]:
                barLength = bar.end - bar.start
                beatLength = barLength / bar.timeSignature.numerator
                for beat in bar.voices[0].beats:
                    beat.measure = bar
                    start = (beat.start - bar.start) / beatLength
                    for note in beat.notes:
                        sound = instrument_track.add_sound(bar, beat, note)
                        if sound:
                            ibeat = int(start) + 1
                            sound['beat'] = ibeat
                            sound['start'] = start - int(start)

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