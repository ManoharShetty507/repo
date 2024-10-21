document.addEventListener("DOMContentLoaded", function() {
  // Fetch and display books
  fetch('/books')
      .then(response => response.json())
      .then(data => {
          const booksList = document.getElementById('books-list');
          data.forEach(book => {
              let listItem = document.createElement('li');
              listItem.textContent = `${book.title} by ${book.author} - $${book.price}`;
              booksList.appendChild(listItem);
          });
      });

  // Fetch and display electronics
  fetch('/electronics')
      .then(response => response.json())
      .then(data => {
          const electronicsList = document.getElementById('electronics-list');
          data.forEach(electronic => {
              let listItem = document.createElement('li');
              listItem.textContent = `${electronic.name} (${electronic.brand}) - $${electronic.price}`;
              electronicsList.appendChild(listItem);
          });
      });

  // Fetch and display household items
  fetch('/household')
      .then(response => response.json())
      .then(data => {
          const householdList = document.getElementById('household-list');
          data.forEach(item => {
              let listItem = document.createElement('li');
              listItem.textContent = `${item.name} (${item.brand}) - $${item.price}`;
              householdList.appendChild(listItem);
          });
      });
});
