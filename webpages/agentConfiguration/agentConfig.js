// Agent Configuration JavaScript
// Handles all the interactive functionality for the agent configuration page

// State management
let agentConfig = {
    name: 'Vermont Destination Expert',
    description: 'An expert agent for recreational and business travelers interested in Vermont.',
    llm: 'gemini-2.0-flash',
    domainKnowledge: {
        skiResorts: true,
        breweries: true,
        hikingTrails: true,
        mapleSyrupProducers: false,
        historicalSites: true,
        artGalleries: false,
    },
    capabilities: {
        webSearch: true,
        dataAnalysis: false,
        imageGeneration: false,
        codeExecution: true,
        apiIntegration: true,
        documentProcessing: false,
    },
    organization: {
        role: 'specialist',
        department: 'customer-service',
        reportingStructure: 'autonomous',
        collaborationLevel: 'medium'
    },
    missions: []
};

// Domain knowledge options
const domainOptions = {
    skiResorts: { label: 'Ski Resorts', icon: 'mountain' },
    breweries: { label: 'Breweries & Distilleries', icon: 'beer' },
    hikingTrails: { label: 'Hiking Trails', icon: 'map' },
    mapleSyrupProducers: { label: 'Maple Syrup Producers', icon: 'leaf' },
    historicalSites: { label: 'Historical Sites', icon: 'landmark' },
    artGalleries: { label: 'Art Galleries & Museums', icon: 'palette' }
};

// Capabilities options
const capabilityOptions = {
    webSearch: { label: 'Web Search', description: 'Search the internet for information' },
    dataAnalysis: { label: 'Data Analysis', description: 'Analyze and interpret data sets' },
    imageGeneration: { label: 'Image Generation', description: 'Create images and visual content' },
    codeExecution: { label: 'Code Execution', description: 'Run and execute code snippets' },
    apiIntegration: { label: 'API Integration', description: 'Connect with external services' },
    documentProcessing: { label: 'Document Processing', description: 'Read and process documents' }
};

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeLucideIcons();
    setupTabNavigation();
    populateDomainKnowledge();
    populateCapabilities();
    populateOrganization();
    populateMissions();
    setupEventListeners();
});

function initializeLucideIcons() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
}

function populateDomainKnowledge() {
    const container = document.getElementById('domainKnowledge');
    
    Object.entries(domainOptions).forEach(([key, option]) => {
        const isChecked = agentConfig.domainKnowledge[key];
        
        const domainItem = document.createElement('div');
        domainItem.className = 'flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50';
        
        domainItem.innerHTML = `
            <input type="checkbox" id="domain-${key}" ${isChecked ? 'checked' : ''} 
                   class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
            <div class="flex items-center space-x-2">
                <i data-lucide="${option.icon}" class="w-4 h-4 text-gray-600"></i>
                <label for="domain-${key}" class="text-sm font-medium text-gray-700 cursor-pointer">
                    ${option.label}
                </label>
            </div>
        `;
        
        container.appendChild(domainItem);
        
        // Add event listener for checkbox
        const checkbox = domainItem.querySelector(`#domain-${key}`);
        checkbox.addEventListener('change', (e) => {
            agentConfig.domainKnowledge[key] = e.target.checked;
            console.log('Domain knowledge updated:', agentConfig.domainKnowledge);
        });
    });
    
    // Reinitialize icons after adding new elements
    initializeLucideIcons();
}

function populateCapabilities() {
    const container = document.getElementById('capabilities');
    
    Object.entries(capabilityOptions).forEach(([key, option]) => {
        const isChecked = agentConfig.capabilities[key];
        
        const capabilityItem = document.createElement('div');
        capabilityItem.className = 'flex items-start space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50';
        
        capabilityItem.innerHTML = `
            <input type="checkbox" id="capability-${key}" ${isChecked ? 'checked' : ''} 
                   class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 mt-1">
            <div class="flex-1">
                <label for="capability-${key}" class="text-sm font-medium text-gray-700 cursor-pointer block">
                    ${option.label}
                </label>
                <p class="text-xs text-gray-500 mt-1">${option.description}</p>
            </div>
        `;
        
        container.appendChild(capabilityItem);
        
        // Add event listener for checkbox
        const checkbox = capabilityItem.querySelector(`#capability-${key}`);
        checkbox.addEventListener('change', (e) => {
            agentConfig.capabilities[key] = e.target.checked;
            console.log('Capabilities updated:', agentConfig.capabilities);
        });
    });
}

function populateOrganization() {
    const container = document.getElementById('organization');
    
    container.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Agent Role</label>
                <select id="agentRole" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="specialist">Specialist</option>
                    <option value="generalist">Generalist</option>
                    <option value="coordinator">Coordinator</option>
                    <option value="supervisor">Supervisor</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Department</label>
                <select id="agentDepartment" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="customer-service">Customer Service</option>
                    <option value="research">Research & Development</option>
                    <option value="operations">Operations</option>
                    <option value="marketing">Marketing</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Reporting Structure</label>
                <select id="reportingStructure" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="autonomous">Autonomous</option>
                    <option value="supervised">Supervised</option>
                    <option value="collaborative">Collaborative</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Collaboration Level</label>
                <select id="collaborationLevel" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                </select>
            </div>
        </div>
    `;
    
    // Set current values
    document.getElementById('agentRole').value = agentConfig.organization.role;
    document.getElementById('agentDepartment').value = agentConfig.organization.department;
    document.getElementById('reportingStructure').value = agentConfig.organization.reportingStructure;
    document.getElementById('collaborationLevel').value = agentConfig.organization.collaborationLevel;
    
    // Add event listeners
    ['agentRole', 'agentDepartment', 'reportingStructure', 'collaborationLevel'].forEach(id => {
        document.getElementById(id).addEventListener('change', (e) => {
            const key = id.replace('agent', '').replace('Agent', '').toLowerCase();
            const actualKey = id === 'agentRole' ? 'role' : 
                             id === 'agentDepartment' ? 'department' :
                             id.replace(/([A-Z])/g, (match, letter) => letter.toLowerCase());
            agentConfig.organization[actualKey] = e.target.value;
            console.log('Organization updated:', agentConfig.organization);
        });
    });
}

function populateMissions() {
    const container = document.getElementById('missions');
    
    container.innerHTML = `
        <div class="space-y-4">
            <div class="flex justify-between items-center">
                <h4 class="text-md font-medium text-gray-900">Active Missions</h4>
                <button id="addMission" class="px-3 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700">
                    Add Mission
                </button>
            </div>
            <div id="missionsList" class="space-y-3">
                <!-- Missions will be populated here -->
            </div>
        </div>
    `;
    
    document.getElementById('addMission').addEventListener('click', addNewMission);
    renderMissions();
}

function addNewMission() {
    const newMission = {
        id: Date.now(),
        title: 'New Mission',
        description: 'Mission description',
        priority: 'medium',
        status: 'active'
    };
    
    agentConfig.missions.push(newMission);
    renderMissions();
}

function renderMissions() {
    const container = document.getElementById('missionsList');
    
    if (agentConfig.missions.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-sm italic">No missions configured yet.</p>';
        return;
    }
    
    container.innerHTML = agentConfig.missions.map(mission => `
        <div class="p-3 border border-gray-200 rounded-lg">
            <div class="flex justify-between items-start">
                <div class="flex-1">
                    <input type="text" value="${mission.title}" 
                           class="font-medium text-gray-900 bg-transparent border-none p-0 focus:outline-none focus:ring-0"
                           onchange="updateMission(${mission.id}, 'title', this.value)">
                    <textarea class="w-full text-sm text-gray-600 bg-transparent border-none p-0 mt-1 resize-none focus:outline-none focus:ring-0"
                              onchange="updateMission(${mission.id}, 'description', this.value)">${mission.description}</textarea>
                </div>
                <button onclick="removeMission(${mission.id})" class="text-red-500 hover:text-red-700">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    initializeLucideIcons();
}

function updateMission(id, field, value) {
    const mission = agentConfig.missions.find(m => m.id === id);
    if (mission) {
        mission[field] = value;
        console.log('Mission updated:', mission);
    }
}

function removeMission(id) {
    agentConfig.missions = agentConfig.missions.filter(m => m.id !== id);
    renderMissions();
}

function setupEventListeners() {
    // Basic info listeners
    document.getElementById('agentName').addEventListener('input', (e) => {
        agentConfig.name = e.target.value;
    });
    
    document.getElementById('agentDescription').addEventListener('input', (e) => {
        agentConfig.description = e.target.value;
    });
    
    document.getElementById('selectedLlm').addEventListener('change', (e) => {
        agentConfig.llm = e.target.value;
    });
}

// Global functions for mission management
window.updateMission = updateMission;
window.removeMission = removeMission;
