import React, { useState } from "react";

function AddTask({ addTask }) { // receiving function as prop from ToDoList.jsx named as addTask
  const [description, setDescription] = useState("");

  const handleSubmit = (e) => { // When Add Task button is clicked
    e.preventDefault();         // prevent page reload
    if (!description.trim()) return alert("Please enter a task!");
    addTask(description); // calling parent function via props defined in ToDoList.jsx named as addTask and passing description as state
    setDescription("");
  };
          
  return (
    <form className="task-form" onSubmit={handleSubmit}> {/* form submission fetches handleSubmit function defined above */}
      <input
        type="text"
        placeholder="Enter your task..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button type="submit">Add Task</button>
    </form>
  );
}

export default AddTask;
