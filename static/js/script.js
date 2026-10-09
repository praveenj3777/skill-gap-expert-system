// script.js - Frontend Dynamic Logic for Skill-Gap Analysis Expert System

let cachedCareers = null;
const PROFICIENCY_SCALE = {
  1: { label: "Beginner", badge: "secondary", desc: "Terminology familiarity; needs close guidance" },
  2: { label: "Basic", badge: "info", desc: "Understands core concepts; handles guided tasks" },
  3: { label: "Intermediate", badge: "warning", desc: "Solves standard problems independently" },
  4: { label: "Advanced", badge: "primary", desc: "In-depth knowledge; complex optimization" },
  5: { label: "Expert", badge: "success", desc: "Comprehensive authority; system architect" }
};

// Preset test scenarios for Viva Demonstration
const PRESETS = {
  test1: {
    name: "Alice",
    career: "data_analyst",
    skills: {
      "Python": 1,
      "SQL": 1,
      "Excel": 2,
      "Statistics": 1,
      "Data Visualization": 1,
      "Power BI": 1
    }
  },
  test2: {
    name: "Bob",
    career: "data_analyst",
    skills: {
      "Python": 5,
      "SQL": 5,
      "Excel": 4,
      "Statistics": 4,
      "Data Visualization": 4,
      "Power BI": 4
    }
  },
  test3: {
    name: "Charlie",
    career: "web_developer",
    skills: {
      "HTML": 4,
      "CSS": 3,
      "JavaScript": 2,
      "Git": 3,
      "Responsive Design": 1,
      "Backend Basics": 1
    }
  },
  test4: {
    name: "Diana",
    career: "ai_ml_engineer",
    skills: {
      "Python": 1,
      "Mathematics & Linear Algebra": 4,
      "Machine Learning Algorithms": 3,
      "Deep Learning": 2,
      "Data Preprocessing": 3,
      "Model Evaluation": 3
    }
  },
  test5: {
    name: "Evan",
    career: "cybersecurity_analyst",
    skills: {
      "Network Security": 2,
      "Linux & Operating Systems": 3,
      "Cryptography Basics": 1,
      "Vulnerability Assessment": 1,
      "Threat Intelligence & SIEM": 2,
      "Security Protocols": 4
    }
  }
};

/**
 * Fetches careers from the backend API if not already cached.
 */
async function fetchCareers() {
  if (cachedCareers) return cachedCareers;
  try {
    const res = await fetch("/api/careers");
    const data = await res.json();
    cachedCareers = data.careers;
    return cachedCareers;
  } catch (err) {
    console.error("Failed to fetch careers from API:", err);
    return null;
  }
}

/**
 * Triggered when user selects a target career from the dropdown.
 */
async function onCareerChange() {
  const select = document.getElementById("career_id");
  if (!select) return;

  const careerId = select.value;
  const careers = await fetchCareers();
  if (!careers || !careers[careerId]) return;

  const career = careers[careerId];

  // Update header text
  const titleElem = document.getElementById("careerTitle");
  const descElem = document.getElementById("careerDescription");
  if (titleElem) titleElem.textContent = career.name;
  if (descElem) descElem.textContent = career.description;

  // Render skill cards with sliders (no demo data prefilled)
  renderSkillCards(career.skills);
}

/**
 * Dynamically builds skill rating cards for the chosen career.
 */
function renderSkillCards(skillsMap, presetValues = null) {
  const container = document.getElementById("skillsContainer");
  if (!container) return;

  container.innerHTML = "";

  Object.entries(skillsMap).forEach(([skillName, spec]) => {
    const reqLevel = spec.required_level;
    // Default initial slider value is 2 (Basic) for fresh start, or the preset value
    const initialVal = presetValues && presetValues[skillName] !== undefined ? presetValues[skillName] : 2;
    const currentMeta = PROFICIENCY_SCALE[initialVal] || PROFICIENCY_SCALE[2];
    const reqMeta = PROFICIENCY_SCALE[reqLevel] || PROFICIENCY_SCALE[4];

    const col = document.createElement("div");
    col.className = "col-md-6";
    col.innerHTML = `
      <div class="skill-input-card h-100">
        <div class="d-flex justify-content-between align-items-start mb-1">
          <div>
            <h6 class="fw-bold mb-0 text-dark">${skillName}</h6>
            <div class="text-muted small" style="font-size: 0.8rem;">${spec.description || ""}</div>
          </div>
          <div class="text-end ps-2">
            <span class="badge bg-light text-primary border border-primary-subtle small">
              Req: ${reqLevel} (${reqMeta.label})
            </span>
          </div>
        </div>

        <div class="mt-3">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <label class="form-label small text-secondary mb-0">Your Rating:</label>
            <span id="badge_${escapeId(skillName)}" class="badge bg-light text-dark border small fw-semibold">
              Level ${initialVal}: ${currentMeta.label}
            </span>
          </div>
          <input type="range" class="form-range mb-1" 
                 id="input_${escapeId(skillName)}" 
                 name="skill_${skillName}" 
                 min="1" max="5" step="1" 
                 value="${initialVal}" 
                 oninput="updateSkillDisplay('${escapeId(skillName)}', this.value)">
          <div class="d-flex justify-content-between text-muted" style="font-size: 0.72rem;">
            <span>1 Beginner</span>
            <span>2 Basic</span>
            <span>3 Interm.</span>
            <span>4 Advanced</span>
            <span>5 Expert</span>
          </div>
        </div>
      </div>
    `;
    container.appendChild(col);
  });
}

/**
 * Escapes characters for HTML IDs.
 */
function escapeId(str) {
  return str.replace(/[^a-zA-Z0-9]/g, "_");
}

/**
 * Updates badge label when a slider moves.
 */
function updateSkillDisplay(safeId, value) {
  const badge = document.getElementById(`badge_${safeId}`);
  const meta = PROFICIENCY_SCALE[value] || PROFICIENCY_SCALE[1];
  if (badge) {
    badge.textContent = `Level ${value}: ${meta.label}`;
  }
}

/**
 * Loads a Viva test preset explicitly when clicked by the user.
 */
async function loadPreset(presetKey) {
  const preset = PRESETS[presetKey];
  if (!preset) return;

  const nameInput = document.getElementById("student_name");
  if (nameInput) nameInput.value = preset.name;

  const careerSelect = document.getElementById("career_id");
  if (careerSelect) {
    careerSelect.value = preset.career;
    const careers = await fetchCareers();
    if (careers && careers[preset.career]) {
      const career = careers[preset.career];
      document.getElementById("careerTitle").textContent = career.name;
      document.getElementById("careerDescription").textContent = career.description;
      renderSkillCards(career.skills, preset.skills);
    }
  }
}

/**
 * Clears form back to fresh empty state.
 */
async function clearForm() {
  const nameInput = document.getElementById("student_name");
  if (nameInput) nameInput.value = "";

  const careerSelect = document.getElementById("career_id");
  if (careerSelect) {
    const careers = await fetchCareers();
    if (careers && careers[careerSelect.value]) {
      renderSkillCards(careers[careerSelect.value].skills);
    }
  }
}

/**
 * Offline Query Assistant Interaction
 */
async function sendChatMessage() {
  const input = document.getElementById("chatInput");
  const msgBox = document.getElementById("chatMessages");
  if (!input || !msgBox) return;

  const query = input.value.trim();
  if (!query) return;

  // Append user bubble
  const userDiv = document.createElement("div");
  userDiv.className = "chat-bubble user-bubble mb-2 p-2 px-3 small";
  userDiv.textContent = query;
  msgBox.appendChild(userDiv);
  input.value = "";
  msgBox.scrollTop = msgBox.scrollHeight;

  // Query offline assistant backend
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: query })
    });
    const data = await res.json();

    const botDiv = document.createElement("div");
    botDiv.className = "chat-bubble bot-bubble mb-2 p-2 px-3 bg-white border rounded small text-dark";
    botDiv.innerHTML = `<strong>Assistant:</strong> ${data.reply}`;
    msgBox.appendChild(botDiv);
    msgBox.scrollTop = msgBox.scrollHeight;
  } catch (err) {
    const errDiv = document.createElement("div");
    errDiv.className = "chat-bubble bot-bubble mb-2 p-2 px-3 bg-white border rounded small text-danger";
    errDiv.textContent = "Error contacting offline assistant.";
    msgBox.appendChild(errDiv);
    msgBox.scrollTop = msgBox.scrollHeight;
  }
}
