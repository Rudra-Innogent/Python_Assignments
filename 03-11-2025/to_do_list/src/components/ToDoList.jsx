import React, { useState, useEffect } from "react";
import AddTask from "./AddTask";
import TaskList from "./TaskList";

function ToDoList() {
  const [tasks, setTasks] = useState([]);

  // Load from localStorage once on mount
  useEffect(() => {  // componentDidMount
    const storedTasks = localStorage.getItem("tasks"); // fetching tasks from localStorage
    if (storedTasks) {
      setTasks(JSON.parse(storedTasks)); // setting tasks state with parsed data from localStorage
    }
  }, []); // empty dependency array to run only once on component mount

  // Save to localStorage whenever tasks change (only if tasks not empty)
  useEffect(() => {  // componentDidUpdate for tasks
    if (tasks.length > 0) {  // to avoid saving empty array on initial load
      localStorage.setItem("tasks", JSON.stringify(tasks)); // saving tasks to localStorage as string
    }
  }, [tasks]); // dependency array with tasks

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
  const addTask = (description) => {  // description received from AddTask.jsx via props named as addTask passed below
    if (!description.trim()) return;
    const newTask = {                 // creating new task object
      id: Date.now(),
      description,
      date: getCurrentDateTime(),
    };
    setTasks((prev) => [...prev, newTask]); // updating tasks state by adding new task to existing tasks then saving to localStorage via useEffect above
  };

  // Update existing task
  const updateTask = (id, newDesc) => { // id and newDesc received from TaskList.jsx via props named as updateTask passed below
    const updated = tasks.map((task) =>  // mapping through existing tasks
      task.id === id
        ? { ...task, description: newDesc, date: getCurrentDateTime() }
        : task
    );
    setTasks(updated);
  };

  // Delete task
  const deleteTask = (id) => {  // id received from TaskList.jsx via props named as deleteTask passed below
    setTasks(tasks.filter((task) => task.id !== id)); // filtering out the task with matching id and updating tasks state then saving to localStorage via useEffect above
  };

  return (
    <div className="todo-container">
      <h1 className="app-title">My To-Do List</h1>
      <AddTask addTask={addTask} />  { /* passing function as prop */}
      <TaskList tasks={tasks} updateTask={updateTask} deleteTask={deleteTask} /> {/* passing functions as props for update and delete */}
    </div>
  );
}

export default ToDoList;
