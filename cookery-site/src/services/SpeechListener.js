
var SpeechListener = function() {
    this.isInitialized = false
    this.isListening = false    
}

SpeechListener.prototype.init = function() {

    if (!this.isInitialized) {

        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
        this.engine = new SpeechRecognition()

        this.engine.interimResults = false
        this.engine.continuous = true
        this.engine.lang = 'de-DE'

        this.engine.onresult = function(event) {
            console.log('you said: ' + event.results[0][0].transcript)
        }
        this.isInitialized = true
    }

    /*this.engine.addEventListener('result', event => {
        const transcript = event.results[0][0].transcript;
            
        console.log('bar');

        // check if the voice input has ended
        if(event.results[0].isFinal) {
          console.log(transcript);
          
          // check if the input starts with 'hello'
          if(transcript.indexOf('hello') == 0) {
            console.log('You said hello to somebody.');
          }
        }
      });*/

      //this.engine.addEventListener('end', this.engine.start);      
}

SpeechListener.prototype.listen = function() {
    if (this.isInitialized) {
        this.engine.isListening = true
        this.engine.start()
    }
}

SpeechListener.prototype.stop = function() {
    if (this.isInitialized) {
        this.engine.abort()
        this.engine.isListening = false
    }
}

export const speechListener = new SpeechListener()