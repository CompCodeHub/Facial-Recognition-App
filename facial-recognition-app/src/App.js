import { useState } from "react";
import { v4 as uuid } from "uuid";
import "./App.css";

function App() {
  const [image, setImage] = useState("");
  const [uploadResultMessage, setUploadResultMessage] = useState(
    "Please upload an image to authenticate"
  );
  const [visitorName, setVisitorName] = useState("placeholder.jpg");
  const [isAuth, setAuth] = useState(false);

  const sendImage = (e) => {
    e.preventDefault();
    setVisitorName(image.name);
    const visitorImageName = uuid();
    fetch("...", {
      method: "PUT",
      headers: {
        "Content-Type": "image/jpeg",
      },
      body: image,
    })
      .then(async () => {
        const response = await authenticate(visitorImageName);
        if (response.Message === "Success") {
          setAuth(true);
          setUploadResultMessage(
            `Hi ${response["firstName"]} ${response["lastName"]} welcome to work`
          );
        } else {
          setAuth(false);
          setUploadResultMessage("Sorry, I don't know you!");
        }
      })
      .catch((err) => {
        setAuth(false);
        setUploadResultMessage(
          "Error: Authentication failed! Please try again!"
        );
      });
  };

  const authenticate = async (visitorImageName) => {
    const requestUrl = "...";

    return await fetch(requestUrl, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => data)
      .catch((err) => console.log(err));
  };

  return (
    <div>
      <h2>Suyash's Facial Rekognition System</h2>
      <form onSubmit={sendImage}>
        <input
          type="file"
          name="image"
          onChane={(e) => setImage(e.target.files[0])}
        />
        <button type="submit">Authenticate</button>
      </form>
      <div className={isAuth ? 'success': 'failure'}>{uploadResultMessage}</div>
      <img
        src={require(`./visitors/${visitorName}`)}
        alt="Visitor"
        height={250}
        width={250}
      />
    </div>
  );
}

export default App;
