import React from "react";
import ToDoList from './components/ToDoList';
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <h1 className="app-title">My To-Do List</h1>
      <ToDoList />
    </div>
  );
}

export default App;
