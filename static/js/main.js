const modal = document.getElementById('taskModal');
const taskForm = document.getElementById('taskForm');
const modalTitle = document.getElementById('modalTitle');
let editingTaskId = null;

function openAddModal() {
    editingTaskId = null;
    modalTitle.textContent = 'Add New Task';
    taskForm.reset();
    taskForm.action = '/task/add';
    modal.classList.add('active');
}

function openEditModal(taskId) {
    editingTaskId = taskId;
    modalTitle.textContent = 'Edit Task';
    
    fetch(`/api/task/${taskId}`)
        .then(response => response.json())
        .then(task => {
            document.getElementById('title').value = task.title;
            document.getElementById('description').value = task.description || '';
            document.getElementById('priority').value = task.priority;
            taskForm.action = `/task/${taskId}/edit`;
            modal.classList.add('active');
        });
}

function closeModal() {
    modal.classList.remove('active');
    editingTaskId = null;
}

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('.theme-icon');
    icon.textContent = theme === 'light' ? '🌙' : '☀️';
}

document.querySelectorAll('.flash-close').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.parentElement.remove();
    });
});

setTimeout(() => {
    document.querySelectorAll('.flash-message').forEach(msg => {
        msg.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => msg.remove(), 300);
    });
}, 5000);
