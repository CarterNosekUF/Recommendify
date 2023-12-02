const input_field = document.querySelector(".input-space");
const logo = document.querySelector(".logo");
const text = document.querySelector(".user-space");
const regex = /^https:\/\/open\.spotify\.com\/playlist\/[a-zA-Z0-9]+$/;

input_field.addEventListener('focus', function () {
  this.placeholder = '';
});

input_field.addEventListener('blur', function () {
  this.placeholder = 'https://open.spotify.com/playlist (unique playlist link)'
});

logo.addEventListener('click', function () {
  location.reload();
});

function linkChecker(string) {
  return regex.test(string);
};


function fetchResponse(string) {
  return fetch('http://127.0.0.1:5000/server', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ data: string }),
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response data
    return data.result;
  })
  .catch(error => {
    console.error('Error:', error);
    throw error; // Re-throw the error to propagate it further
  });
}


document.addEventListener('keyup', async (event) => {

  if (event.key == "Enter"){
    text.textContent = "loading"

    try {
      const result = await fetchResponse(input_field.value);
      text.textContent = result; // Update the text with the fetched result
    } catch (error) {
      text.textContent = error; // Handle errors
      console.error('Error:', error);
    }
  }
  /*if (!regex.test(input_field.value)) {
    input_field.style.outlineColor = "red";
    input_field.style.outlineWidth = "1px";
    input_field.style.outlineStyle = "solid"
  }
  else {
    input_field.style.outlineColor = "#1DB954";
    input_field.style.outlineWidth = "1px";
    input_field.style.outlineStyle = "solid"
  }*/
});

fetch('http://127.0.0.1:5000/server', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ data: inputData }),
})
.then(response => response.json())
.then(data => {
    // Handle the response data
    document.getElementById('result').innerText = 'Result: ' + data.result;
    console.log('Additional Response:', data.additionalResponse);
})
.catch(error => console.error('Error:', error));
