const topicInput = document.getElementById('topic');
const depthRadios = document.querySelectorAll('input[name="depth"]');
const includeMediaCheckbox = document.getElementById('includeMedia');
const startBtn = document.getElementById('startBtn');
const relatedBtn = document.getElementById('relatedBtn');
const loading = document.getElementById('loading');
const loadingText = document.getElementById('loadingText');
const progressFill = document.getElementById('progressFill');
const results = document.getElementById('results');
const stages = document.getElementById('stages');
const finalReport = document.getElementById('finalReport');
const totalTime = document.getElementById('totalTime');
const relatedTopics = document.getElementById('relatedTopics');
const topicsList = document.getElementById('topicsList');
const mediaSection = document.getElementById('mediaSection');
const mediaContent = document.getElementById('mediaContent');
const copyBtn = document.getElementById('copyBtn');
const printBtn = document.getElementById('printBtn');
const downloadBtn = document.getElementById('downloadBtn');

// Depth card selection
document.querySelectorAll('.depth-card').forEach(card => {
    card.addEventListener('click', () => {
        document.querySelectorAll('.depth-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        card.querySelector('input[type="radio"]').checked = true;
    });
});

const stageMessages = [
    {
        text: "🔍 Research Agent analyzing topic...",
        progress: 25
    },
    {
        text: "📊 Analyst Agent extracting insights...",
        progress: 50
    },
    {
        text: "🎯 Critic Agent reviewing findings...",
        progress: 75
    },
    {
        text: "✨ Synthesizer Agent creating final report...",
        progress: 100
    }
];

let currentStage = 0;
let loadingInterval;

startBtn.addEventListener('click', async () => {
    const topic = topicInput.value.trim();
    if (!topic) {
        showNotification('Please enter a research topic', 'warning');
        topicInput.focus();
        return;
    }

    const selectedDepth = document.querySelector('input[name="depth"]:checked').value;
    const includeMedia = includeMediaCheckbox.checked;

    // Reset
    results.style.display = 'none';
    relatedTopics.style.display = 'none';
    mediaSection.style.display = 'none';
    loading.style.display = 'block';
    startBtn.disabled = true;
    currentStage = 0;
    stages.innerHTML = '';

    // Animate loading messages
    loadingInterval = setInterval(() => {
        if (currentStage < stageMessages.length) {
            loadingText.textContent = stageMessages[currentStage].text;
            progressFill.style.width = stageMessages[currentStage].progress + '%';
            currentStage++;
        }
    }, 2000);

    try {
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                topic: topic,
                depth: selectedDepth,
                include_media: includeMedia
            })
        });

        clearInterval(loadingInterval);

        if (!response.ok) {
            throw new Error('Research failed');
        }

        const data = await response.json();
        displayResults(data);
        showNotification('Research completed successfully!', 'success');

    } catch (error) {
        clearInterval(loadingInterval);
        showNotification('Error: ' + error.message, 'error');
        console.error(error);
    } finally {
        loading.style.display = 'none';
        startBtn.disabled = false;
    }
});

relatedBtn.addEventListener('click', async () => {
    const topic = topicInput.value.trim();
    if (!topic) {
        showNotification('Please enter a topic first', 'warning');
        topicInput.focus();
        return;
    }

    relatedBtn.disabled = true;
    relatedBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Finding...';

    try {
        const response = await fetch('/api/related-topics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic: topic })
        });

        const data = await response.json();
        displayRelatedTopics(data.topics);

    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        relatedBtn.disabled = false;
        relatedBtn.innerHTML = '<i class="fas fa-network-wired"></i> Find Related Topics';
    }
});

function displayResults(data) {
    results.style.display = 'block';
    totalTime.textContent = `${data.total_time.toFixed(2)}s`;

    // Display stages
    stages.innerHTML = '';
    data.stages.forEach((stage, index) => {
        const stageDiv = document.createElement('div');
        stageDiv.className = 'stage';
        stageDiv.style.animationDelay = `${index * 0.1}s`;
        
        const icon = getStageIcon(stage.name);
        
        stageDiv.innerHTML = `
            <div class="stage-header">
                <span class="stage-title">${icon} ${index + 1}. ${stage.name}</span>
                <span class="stage-agent">${stage.agent}</span>
            </div>
            <div class="stage-content">${escapeHtml(stage.output)}</div>
        `;
        stages.appendChild(stageDiv);
    });

    // Display final report
    finalReport.innerHTML = formatMarkdown(data.final_report);

    // Display media if available
    if (data.media && data.media.length > 0) {
        displayMedia(data.media);
    }

    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function displayMedia(mediaItems) {
    mediaSection.style.display = 'block';
    mediaContent.innerHTML = '';
    
    mediaItems.forEach(item => {
        const mediaDiv = document.createElement('div');
        mediaDiv.className = 'media-item';
        mediaDiv.innerHTML = `
            <div class="media-item-content">
                <i class="fas ${item.type === 'video' ? 'fa-video' : 'fa-image'}" style="font-size: 3em; color: var(--primary); margin-bottom: 15px;"></i>
                <h4>${item.title}</h4>
                <p>${item.description}</p>
                <p style="margin-top: 10px; font-size: 0.85em;"><strong>Suggested search:</strong> ${item.query}</p>
            </div>
        `;
        mediaContent.appendChild(mediaDiv);
    });
}

function displayRelatedTopics(topics) {
    relatedTopics.style.display = 'block';
    topicsList.innerHTML = '';
    
    const icons = ['fa-lightbulb', 'fa-atom', 'fa-rocket', 'fa-brain', 'fa-microscope'];
    
    topics.forEach((topic, index) => {
        const topicCard = document.createElement('div');
        topicCard.className = 'topic-card';
        topicCard.innerHTML = `
            <i class="fas ${icons[index % icons.length]}"></i>
            <span>${topic}</span>
        `;
        topicCard.addEventListener('click', () => {
            topicInput.value = topic;
            relatedTopics.style.display = 'none';
            topicInput.scrollIntoView({ behavior: 'smooth' });
            showNotification(`Topic selected: ${topic}`, 'info');
        });
        topicsList.appendChild(topicCard);
    });
    
    relatedTopics.scrollIntoView({ behavior: 'smooth' });
}

function getStageIcon(stageName) {
    const icons = {
        'Research': '<i class="fas fa-search"></i>',
        'Analysis': '<i class="fas fa-chart-bar"></i>',
        'Critique': '<i class="fas fa-balance-scale"></i>',
        'Final Synthesis': '<i class="fas fa-file-contract"></i>'
    };
    return icons[stageName] || '<i class="fas fa-cog"></i>';
}

// Copy report
copyBtn?.addEventListener('click', () => {
    const text = finalReport.innerText;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Report copied to clipboard!', 'success');
    });
});

// Print report
printBtn?.addEventListener('click', () => {
    window.print();
});

// Download report
downloadBtn?.addEventListener('click', () => {
    const text = finalReport.innerText;
    const blob = new Blob([text], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `research-report-${Date.now()}.md`;
    a.click();
    showNotification('Report downloaded!', 'success');
});

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatMarkdown(text) {
    text = escapeHtml(text);
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    text = text.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    text = text.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    text = text.replace(/\n\n/g, '<br><br>');
    text = text.replace(/\n/g, '<br>');
    return text;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideInRight 0.3s;
        font-weight: 600;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);