

var SpeechSynth = function() {

    this.engine = window.speechSynthesis
    this.voices = this.engine.getVoices()

    this.speechOutput = new window.SpeechSynthesisUtterance()
}

SpeechSynth.prototype.say = function(message) {
    this.speechOutput.text = message

    this.speechOutput.voice = this.voices[0]
    this.engine.speak(this.speechOutput)

}

export const speechSynth = new SpeechSynth()