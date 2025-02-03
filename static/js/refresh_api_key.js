document
  .getElementById("refresh-api-key-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    fetch("/refresh_api_key", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector('input[name="csrf_token"]').value,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("api-key").textContent = data.api_key;
        document.getElementById("api-key-expiration").textContent =
          data.api_key_expiration;
      })
      .catch((error) => console.error("Error:", error));
  });
