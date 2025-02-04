document.addEventListener("DOMContentLoaded", function () {
  const codeSnippetField = document.getElementById("code_snippet");

  codeSnippetField.addEventListener("keydown", function (event) {
    if (event.key === "Tab") {
      event.preventDefault();
      const start = this.selectionStart;
      const end = this.selectionEnd;

      // Set textarea value to: text before caret + tab + text after caret
      this.value =
        this.value.substring(0, start) + "\t" + this.value.substring(end);

      // Put caret at right position again
      this.selectionStart = this.selectionEnd = start + 1;
    }
  });
});
