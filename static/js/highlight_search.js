document
  .getElementById("search-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const searchTerm = document
      .getElementById("search-input")
      .value.trim()
      .toLowerCase();
    if (!searchTerm) {
      return;
    }

    // Remove existing highlights
    document.querySelectorAll(".highlight").forEach(function (element) {
      const parent = element.parentNode;
      parent.replaceChild(
        document.createTextNode(element.textContent),
        element
      );
      parent.normalize();
    });

    // Function to highlight text nodes
    function highlightTextNodes(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        const text = node.textContent.toLowerCase();
        const index = text.indexOf(searchTerm);
        if (index !== -1) {
          const span = document.createElement("span");
          span.className = "highlight";
          const highlightedText = node.splitText(index);
          highlightedText.splitText(searchTerm.length);
          const highlightedClone = highlightedText.cloneNode(true);
          span.appendChild(highlightedClone);
          highlightedText.parentNode.replaceChild(span, highlightedText);
        }
      } else if (
        node.nodeType === Node.ELEMENT_NODE &&
        node.childNodes &&
        !["SCRIPT", "STYLE", "NOSCRIPT"].includes(node.tagName)
      ) {
        node.childNodes.forEach(highlightTextNodes);
      }
    }

    // Start highlighting from the body element
    highlightTextNodes(document.body);
  });
