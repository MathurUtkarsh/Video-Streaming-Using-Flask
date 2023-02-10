from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)


def generate_frames():
    while True:

        ## read the camera frame

        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # To pass it index.html we have to use buffer and convert it into bytes.

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # From open-cv Documentation Page.


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

## mimetype is required for continuous input or response.

if __name__ == "__main__":
    app.run(debug=True)