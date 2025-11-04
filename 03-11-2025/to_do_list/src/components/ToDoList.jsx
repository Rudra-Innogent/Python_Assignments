import React, { useState, useEffect } from "react";
import AddTask from "./AddTask";
import TaskList from "./TaskList";

function ToDoList() {
  // Initialize from localStorage safely
  const [tasks, setTasks] = useState(() => {
    const savedTasks = localStorage.getItem("tasks");
    return savedTasks ? JSON.parse(savedTasks) : [];
  });

  // Whenever tasks update → save to localStorage
  useEffect(() => {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }, [tasks]);

  // Add new task
  const addTask = (description) => {
    const newTask = {
      id: Date.now(),
      date: new Date().toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false, // 24-hour format
      }),
      description,
    };
    setTasks((prev) => [...prev, newTask]);
  };

  // Delete task
  const deleteTask = (id) => {
    setTasks((prev) => prev.filter((task) => task.id !== id));
  };

  // Update task
 // Update task
const updateTask = (id, newDesc) => {
  setTasks((prev) =>
    prev.map((task) =>
      task.id === id
        ? {
            ...task,
            description: newDesc,
            date: new Date().toLocaleString("en-IN", {
              day: "2-digit",
              month: "short",
              year: "numeric",
              hour: "2-digit",
              minute: "2-digit",
              hour12: false, // 24-hour format
            }),
          }
        : task
    )
  );
};


  return (
    <div className="todo-container">
      <AddTask addTask={addTask} />
      <TaskList tasks={tasks} deleteTask={deleteTask} updateTask={updateTask} />
    </div>
  );
}

export default ToDoList;
