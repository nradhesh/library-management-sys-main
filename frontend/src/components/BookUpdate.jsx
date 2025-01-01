import React, { useEffect, useState } from "react";
import axios from "../api/axios";

function BookList() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    axios.get("/books")
      .then(response => setBooks(response.data))
      .catch(error => console.error("Error fetching books:", error));
  }, []);

  return (
    <div>
      <h2>Books</h2>
      <ul>
        {books.map(book => (
          <li key={book.id}>
            {book.title} by {book.author} (ISBN: {book.isbn}) - {book.available ? "Available" : "Not Available"}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BookList;