# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from text2speech.modules import TTS, TTSValidator
from voxpopuli import Voice
from tempfile import gettempdir
from os.path import join
from text2speech.util import LOG


class MbrolaTTS(TTS):
    audio_ext = "wav"

    def __init__(self, config=None):
        config = config or {"lang": "en"}
        super(MbrolaTTS, self).__init__(config, MbrolaValidator(self))
        # TODO ssml tags ?
        self.lang = self.lang.split("-")[0]
        self.speed = self.config.get("speed", 160)  # word per minute
        self.pitch = self.config.get("pitch", 50)
        self.volume = self.config.get("volume")  # float 0 - 1
        self.voice_id = self.config.get("voice_id")

    def get_voice(self):
        return Voice(lang=self.lang, pitch=self.pitch, speed=self.speed,
                     voice_id=self.voice_id, volume=self.volume)

    def _get_phonemes(self, utterance):
        voice = self.get_voice()
        return [(phoneme.name, phoneme.duration) for
                phoneme in voice.to_phonemes(utterance)]

    def _get_wav(self, utterance, out_file=None):
        voice = self.get_voice()
        wav = voice.to_audio(utterance)
        if out_file is None:
            out_file = join(gettempdir(), "voxpopuli.wav")
        with open(out_file, "wb") as wavfile:
            wavfile.write(wav)
        return out_file

    def modify_tag(self, tag):
        """Override to modify each supported ssml tag"""
        if "%" in tag:
            if "-" in tag:
                val = tag.split("-")[1].split("%")[0]
                tag = tag.replace("-", "").replace("%", "")
                new_val = int(val) / 100
                tag = tag.replace(val, new_val)
            elif "+" in tag:
                val = tag.split("+")[1].split("%")[0]
                tag = tag.replace("+", "").replace("%", "")
                new_val = int(val) / 100
                tag = tag.replace(val, new_val)
        return tag

    def get_tts(self, sentence, wav_file):
        wav_file = self._get_wav(sentence, wav_file)
        # TODO phonemes
        return wav_file, None

    def describe_voices(self):
        return self.get_voice().listvoices()


class MbrolaValidator(TTSValidator):
    def __init__(self, tts):
        super(MbrolaValidator, self).__init__(tts)

    def validate_lang(self):
        langs = self.tts.describe_voices()
        if self.tts.lang not in langs:
            LOG.error("Unsupported language, choose one of {langs}".
                      format(langs=list(langs.keys())))
            raise ValueError
        if self.tts.voice_id is not None:
            if self.tts.voice_id not in langs[self.tts.lang]:
                LOG.error("Unsupported voice id, choose one of {langs} or "
                          "unset this value to use defaults".
                          format(langs=langs[self.tts.lang]))
                raise ValueError

    def validate_connection(self):
        self.tts.get_voice()

    def get_tts_class(self):
        return MbrolaTTS
