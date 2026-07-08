const ROLES = [
  'Student',
  'Faculty',
  'Leadership',
  'Business Affairs',
  'Communications'
];

const QUESTIONS = [
  {
    id: 1,
    text: 'Does your institution have clear AI policies, academic integrity guidance, or governance frameworks in place?',
    dimension: 'Governance & Policy',
    choices: {
      A: [3, 'Yes, clear policies and governance are established.'],
      B: [2, 'Some policies exist, but they are not consistently communicated.'],
      C: [1, 'Policy guidance is emerging but not widely available.'],
      D: [0, 'There are no formal AI policies or governance structures yet.']
    }
  },
  {
    id: 2,
    text: 'Do stakeholders in your unit have reliable access to AI tools, platforms, or infrastructure to support teaching, learning, or administration?',
    dimension: 'Systems & Infrastructure',
    choices: {
      A: [3, 'Yes, people have consistent access to AI tools and infrastructure.'],
      B: [2, 'Access exists but is limited to certain units or services.'],
      C: [1, 'Access is inconsistent and often depends on individual effort.'],
      D: [0, 'There is little or no access to AI tools or infrastructure.']
    }
  },
  {
    id: 3,
    text: 'How well do stakeholders understand the implications of AI for teaching, research, student services, or operations?',
    dimension: 'Culture & Skills',
    choices: {
      A: [3, 'Many people have a strong understanding of AI opportunities and risks.'],
      B: [2, 'There is some awareness, though knowledge is uneven.'],
      C: [1, 'Only a few people understand AI implications clearly.'],
      D: [0, 'AI awareness and skills are very low across the institution.']
    }
  },
  {
    id: 4,
    text: 'Is there ongoing training or support for AI literacy, ethical use, and responsible adoption?',
    dimension: 'Education & Training',
    choices: {
      A: [3, 'Yes, there is structured training and support for AI literacy.'],
      B: [2, 'Some training exists but it is not comprehensive.'],
      C: [1, 'Training is available only informally or on request.'],
      D: [0, 'There is no training or support for AI literacy yet.']
    }
  },
  {
    id: 5,
    text: 'Does leadership actively sponsor AI readiness initiatives and allocate resources for implementation?',
    dimension: 'Governance & Policy',
    choices: {
      A: [3, 'Leadership is actively sponsoring AI initiatives with clear resources.'],
      B: [2, 'Leadership shows some interest but resourcing is uneven.'],
      C: [1, 'Leadership support is limited and not well-coordinated.'],
      D: [0, 'Leadership has not yet committed resources to AI readiness.']
    }
  },
  {
    id: 6,
    text: 'Are AI technologies integrated into workflows and systems with attention to security, privacy, and ethical risks?',
    dimension: 'Systems & Infrastructure',
    choices: {
      A: [3, 'Yes, AI systems are integrated with strong security and privacy practices.'],
      B: [2, 'Integration exists but governance or risk practices are still developing.'],
      C: [1, 'AI technologies are used with inconsistent risk management.'],
      D: [0, 'AI tools are used without formal security or privacy controls.']
    }
  },
  {
    id: 7,
    text: 'Do departments share AI knowledge, coordinate projects, and involve multiple stakeholders in planning?',
    dimension: 'Culture & Skills',
    choices: {
      A: [3, 'Yes, there is active collaboration and stakeholder involvement.'],
      B: [2, 'There is some cross-unit sharing, but it is not consistent.'],
      C: [1, 'Collaboration is rare and mostly informal.'],
      D: [0, 'Units work in isolation with little shared AI planning.']
    }
  },
  {
    id: 8,
    text: 'Does your institution provide role-specific guidance for students, faculty, and staff on responsible AI use?',
    dimension: 'Education & Training',
    choices: {
      A: [3, 'Yes, there is clear, role-specific guidance for different stakeholders.'],
      B: [2, 'Some guidance exists but it is broad rather than role-specific.'],
      C: [1, 'Guidance is minimal and general rather than tailored.'],
      D: [0, 'There is no stakeholder-specific guidance available.']
    }
  }
];

const RECOMMENDATIONS = {
  'Governance & Policy': [
    'Clarify AI ethics, academic integrity, and governance policies for all stakeholders.',
    'Establish a cross-functional AI readiness committee with student, faculty, and administrative representation.',
    'Document and communicate policy expectations for AI tool use in teaching and research.'
  ],
  'Systems & Infrastructure': [
    'Assess current AI tool access and prioritize investments in secure, privacy-aware platforms.',
    'Align AI system integration with existing LMS, SIS, and administrative workflows.',
    'Build a simple roadmap for infrastructure improvements and AI-supported services.'
  ],
  'Culture & Skills': [
    'Offer targeted awareness sessions that explain AI potentials, limitations, and ethical concerns.',
    'Create communities of practice where stakeholders can share AI experiences and use cases.',
    'Encourage leadership messaging that emphasizes responsible AI adoption.'
  ],
  'Education & Training': [
    'Develop introductory AI literacy modules for students, faculty, and staff.',
    'Provide role-specific training on AI in pedagogy, research workflows, and business processes.',
    'Build a review cycle to update training materials as AI norms and tools evolve.'
  ]
};

const dimensions = ['Governance & Policy', 'Systems & Infrastructure', 'Culture & Skills', 'Education & Training'];

function normalizeScore(value) {
  return Number(((value / 3) * 100).toFixed(1));
}

function readinessLevel(rawAverage) {
  if (rawAverage >= 2.5) return 'High';
  if (rawAverage >= 1.5) return 'Moderate';
  return 'Developing';
}

function calculateScores(answers) {
  const dimensionScores = {};
  dimensions.forEach((dimension) => {
    dimensionScores[dimension] = [];
  });

  Object.entries(answers).forEach(([questionId, choiceKey]) => {
    const question = QUESTIONS.find((q) => q.id === Number(questionId));
    if (!question) return;
    const [value] = question.choices[choiceKey];
    dimensionScores[question.dimension].push(value);
  });

  const dimensionSummary = {};
  dimensions.forEach((dimension) => {
    const values = dimensionScores[dimension];
    if (values.length) {
      const average = values.reduce((sum, value) => sum + value, 0) / values.length;
      dimensionSummary[dimension] = {
        raw: Number(average.toFixed(2)),
        percent: normalizeScore(average)
      };
    } else {
      dimensionSummary[dimension] = { raw: 0, percent: 0.0 };
    }
  });

  const overallRaw = dimensions.reduce((sum, dimension) => sum + dimensionSummary[dimension].raw, 0) / dimensions.length;
  return {
    dimensions: dimensionSummary,
    overall: {
      raw: Number(overallRaw.toFixed(2)),
      percent: normalizeScore(overallRaw),
      level: readinessLevel(overallRaw)
    }
  };
}

function summarizeRecommendations(scores) {
  const recs = [];
  Object.entries(scores.dimensions).forEach(([dimension, dimensionScores]) => {
    if (dimensionScores.percent < 70) {
      recs.push(`${dimension}: ${RECOMMENDATIONS[dimension][0]}`);
    }
  });
  if (!recs.length) {
    recs.push('Your institution shows strong readiness indicators. Continue reinforcing governance, infrastructure, culture, and training.');
  }
  return recs;
}

function chatbotResponse(message, role, scores) {
  const text = (message || '').trim().toLowerCase();
  if (!text) {
    return 'Please type a question or ask for recommendations.';
  }
  if (text.includes('what is ai readiness') || text.includes('ai readiness')) {
    return 'AI readiness measures how prepared your institution is to integrate AI responsibly across governance, infrastructure, culture, and training.';
  }
  if (text.includes('governance')) {
    return 'Governance readiness is about policies, ethical frameworks, and clear guidance for stakeholders on responsible AI use.';
  }
  if (text.includes('infrastructure') || text.includes('systems')) {
    return 'Infrastructure readiness covers access to AI tools, secure systems, and data practices that support teaching, research, and administration.';
  }
  if (text.includes('training') || text.includes('education') || text.includes('skills')) {
    return 'Training readiness means providing AI literacy, role-specific guidance, and continuous support for students, faculty, and staff.';
  }
  if (text.includes('recommend') || text.includes('improve') || text.includes('next step')) {
    return 'Evaluate the dimensions where your score is below 70% and prioritize governance, infrastructure, or training improvements accordingly.';
  }
  if (text.includes('score') || text.includes('result')) {
    return `Your current score is ${scores.overall.percent}% with readiness level ${scores.overall.level}.`;
  }
  if (text.includes('student') || text.includes('faculty') || text.includes('leadership') || text.includes('business') || text.includes('communications')) {
    return `As a ${role}, focus on how your role-specific needs align with governance, infrastructure, culture, and training in your unit.`;
  }
  return 'This prototype can answer questions about readiness dimensions, scores, and recommendations. Try asking about governance, infrastructure, or training.';
}

function renderQuestions() {
  const questionsContainer = document.getElementById('questions');
  questionsContainer.innerHTML = '';
  QUESTIONS.forEach((question) => {
    const questionEl = document.createElement('div');
    questionEl.className = 'question';
    questionEl.innerHTML = `<p><strong>${question.id}.</strong> ${question.text}</p>`;

    Object.entries(question.choices).forEach(([key, pair]) => {
      const label = document.createElement('label');
      label.innerHTML = `<input type="radio" name="q_${question.id}" value="${key}" required> ${key}. ${pair[1]}`;
      questionEl.appendChild(label);
      questionEl.appendChild(document.createElement('br'));
    });

    questionsContainer.appendChild(questionEl);
  });
}

function renderRoleOptions() {
  const roleSelect = document.getElementById('role');
  roleSelect.innerHTML = '';
  ROLES.forEach((role) => {
    const option = document.createElement('option');
    option.value = role;
    option.textContent = role;
    roleSelect.appendChild(option);
  });
}

function showSection(id) {
  document.getElementById('assessment-section').classList.toggle('hidden', id !== 'assessment-section');
  document.getElementById('results-section').classList.toggle('hidden', id !== 'results-section');
}

function appendMessage(who, text) {
  const chatbox = document.getElementById('chatbox');
  const p = document.createElement('p');
  p.innerHTML = `<strong>${who}:</strong> ${text}`;
  chatbox.appendChild(p);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function init() {
  renderRoleOptions();
  renderQuestions();
  showSection('assessment-section');

  const form = document.getElementById('assessment-form');
  const backButton = document.getElementById('back');
  const sendButton = document.getElementById('send');

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const answers = {};
    QUESTIONS.forEach((question) => {
      const value = formData.get(`q_${question.id}`);
      if (value) answers[question.id] = value;
    });
    const role = formData.get('role');
    const scores = calculateScores(answers);
    const recommendations = summarizeRecommendations(scores);

    document.getElementById('result-role').textContent = role;
    document.getElementById('result-level').textContent = scores.overall.level;
    document.getElementById('result-percent').textContent = scores.overall.percent;

    const dims = document.getElementById('dimension-list');
    dims.innerHTML = '';
    Object.entries(scores.dimensions).forEach(([dim, value]) => {
      const li = document.createElement('li');
      li.textContent = `${dim}: ${value.percent}%`;
      dims.appendChild(li);
    });

    const recList = document.getElementById('recommendation-list');
    recList.innerHTML = '';
    recommendations.forEach((rec) => {
      const li = document.createElement('li');
      li.textContent = rec;
      recList.appendChild(li);
    });

    document.getElementById('chatbox').innerHTML = '';
    appendMessage('Agent', 'Hi! Ask me about your score, governance, infrastructure, or training.');

    sendButton.onclick = async () => {
      const messageInput = document.getElementById('message');
      const message = messageInput.value.trim();
      if (!message) return;
      appendMessage('You', message);
      messageInput.value = '';

      if (window.CHAT_API_URL) {
        try {
          const resp = await fetch(window.CHAT_API_URL + '/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, role, scores })
          });
          const data = await resp.json();
          appendMessage('Agent', data.response || 'No response from server.');
          return;
        } catch (e) {
          // fall back to local rule-based assistant
        }
      }

      const response = chatbotResponse(message, role, scores);
      appendMessage('Agent', response);
    };

    showSection('results-section');
  });

  backButton.addEventListener('click', () => {
    showSection('assessment-section');
    document.getElementById('message').value = '';
    document.getElementById('chatbox').innerHTML = '';
  });
}

window.addEventListener('DOMContentLoaded', init);
