// console.log("ToDo App JavaScript Loaded...");

document.addEventListener("DOMContentLoaded", fetchTasks);

async function fetchTasks() {
    const response = await fetch('/api/tasks');
    const result = await response.json();
    
    const tbody = document.getElementById("taskTableBody");
    const table = document.getElementById("taskTableElement");
    const clearBtn = document.getElementById("clearButtonWrapper");
    const noTasksMsg = document.getElementById("noTasksMessage");
    
    tbody.innerHTML = ""; // Clear existing rows
    
    if (!result.data || result.data.length === 0) {
        table.style.display = "none";
        clearBtn.style.display = "none";
        noTasksMsg.style.display = "block";
        return;
    }
    
    table.style.display = "table";
    clearBtn.style.display = "block";
    noTasksMsg.style.display = "none";
    
    result.data.forEach(task => {
        const tr = document.createElement("tr");
        
        // Fills the cells with your exact structural CSS classes from the image
        tr.innerHTML = `
            <td>${task.id}</td>
            <td>${task.title}</td>
            <td>
                <span class="badge ${task.status.toLowerCase()}">${task.status}</span>
            </td>
            <td>
                <button type="button" class="btn-small" onclick="toggleTask(${task.id})">Next</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function addNewTask() {
    const input = document.getElementById("taskInput");
    if (!input.value.trim()) return;

    await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: input.value })
    });
    
    input.value = "";
    fetchTasks();
}

async function toggleTask(id) {
    const response = await fetch(`/api/tasks/toggle/${id}`, { method: 'PUT' });
    const result = await response.json();
    
    // If backend indicates all tasks are completed and user is logged out
    if (result.logged_out) {
        const table = document.getElementById("taskTableElement");
        const clearBtn = document.getElementById("clearButtonWrapper");
        
        // Triggers the smooth 1-second fade-out layout transition
        table.classList.add("fade-out-active");
        if (clearBtn) clearBtn.classList.add("fade-out-active");
        
        // Wait 1 second for the animation to end, then show alert and kick out to login
        setTimeout(() => {
            alert("🎉 All tasks completed! \nYou have been automatically logged out. \nPlz login again to add more tasks! 🙏");
            window.location.href = "/login"; // Redirects to your Sagar Chouksey login route portal
        }, 1000);
        
    } else {
        // Standard non-completion step: refresh rows normally
        fetchTasks();
    }
}

async function clearAllTasks() {
    if (confirm("Are you sure you want to clear all tasks?")) {
        await fetch('/api/tasks/clean', { method: 'DELETE' });
        fetchTasks();
    }
}

