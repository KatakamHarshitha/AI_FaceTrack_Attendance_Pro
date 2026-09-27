import cv2
import os


def capture_faces(user_id):
    camera = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    os.makedirs("dataset", exist_ok=True)

    count = 0

    while True:
        success, frame = camera.read()

        if not success:
            print("Could not read camera")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, width, height) in faces:
            count += 1

            face_image = gray[y:y + height, x:x + width]

            file_path = f"dataset/user_{user_id}_{count}.jpg"
            cv2.imwrite(file_path, face_image)

            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Image: {count}/20",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        cv2.imshow("Capture Face", frame)

        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

        if count >= 20:
            break

    camera.release()
    cv2.destroyAllWindows()

    print(f"Captured {count} face images")

def train_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []

    for filename in os.listdir("dataset"):
        if filename.endswith(".jpg"):
            image_path = os.path.join("dataset", filename)

            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            # Extract user ID from filename: user_1_5.jpg
            user_id = int(filename.split("_")[1])

            faces.append(image)
            labels.append(user_id)

    if not faces:
        print("No face images found")
        return

    recognizer.train(faces, __import__("numpy").array(labels))

    recognizer.write("face_model.yml")

    print("Face recognizer trained successfully")

if __name__ == "__main__":
    train_recognizer()