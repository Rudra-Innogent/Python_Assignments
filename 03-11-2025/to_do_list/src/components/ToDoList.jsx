import React, { useState, useEffect } from "react";
import AddTask from "./AddTask";
import TaskList from "./TaskList";

function ToDoList() {
  const [tasks, setTasks] = useState([]);

  // Load from localStorage once on mount
  useEffect(() => {
    const storedTasks = localStorage.getItem("tasks");
    if (storedTasks) {
      setTasks(JSON.parse(storedTasks));
    }
  }, []);

  // Save to localStorage whenever tasks change (only if tasks not empty)
  useEffect(() => {
    if (tasks.length > 0) {
      localStorage.setItem("tasks", JSON.stringify(tasks));
    }
  }, [tasks]);

  // Get current date/time
  const getCurrentDateTime = () => {
    return new Date().toLocaleString("en-GB", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
  };

  // Add new task
  const addTask = (description) => {
    if (!description.trim()) return;
    const newTask = {
      id: Date.now(),
      description,
      date: getCurrentDateTime(),
    };
    setTasks((prev) => [...prev, newTask]);
  };

  // Update existing task
  const updateTask = (id, newDesc) => {
    const updated = tasks.map((task) =>
      task.id === id
        ? { ...task, description: newDesc, date: getCurrentDateTime() }
        : task
    );
    setTasks(updated);
  };

  // Delete task
  const deleteTask = (id) => {
    setTasks(tasks.filter((task) => task.id !== id));
  };

  return (
    <div className="todo-container">
      <h1 className="app-title">My To-Do List</h1>
      <AddTask addTask={addTask} />
      <TaskList tasks={tasks} updateTask={updateTask} deleteTask={deleteTask} />
    </div>
  );
}

export default ToDoList;
