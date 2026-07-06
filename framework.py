STAKEHOLDER_ROLES = [
    "Student",
    "Faculty",
    "Leadership",
    "Business Affairs",
    "Communications"
]

DIMENSIONS = [
    "Governance & Policy",
    "Systems & Infrastructure",
    "Culture & Skills",
    "Education & Training"
]

QUESTIONS = [
    {
        "id": 1,
        "text": "Does your institution have clear AI policies, academic integrity guidance, or governance frameworks in place?",
        "dimension": "Governance & Policy",
        "choices": {
            "A": (3, "Yes, clear policies and governance are established."),
            "B": (2, "Some policies exist, but they are not consistently communicated."),
            "C": (1, "Policy guidance is emerging but not widely available."),
            "D": (0, "There are no formal AI policies or governance structures yet.")
        }
    },
    {
        "id": 2,
        "text": "Do stakeholders in your unit have reliable access to AI tools, platforms, or infrastructure to support teaching, learning, or administration?",
        "dimension": "Systems & Infrastructure",
        "choices": {
            "A": (3, "Yes, people have consistent access to AI tools and infrastructure."),
            "B": (2, "Access exists but is limited to certain units or services."),
            "C": (1, "Access is inconsistent and often depends on individual effort."),
            "D": (0, "There is little or no access to AI tools or infrastructure.")
        }
    },
    {
        "id": 3,
        "text": "How well do stakeholders understand the implications of AI for teaching, research, student services, or operations?",
        "dimension": "Culture & Skills",
        "choices": {
            "A": (3, "Many people have a strong understanding of AI opportunities and risks."),
            "B": (2, "There is some awareness, though knowledge is uneven."),
            "C": (1, "Only a few people understand AI implications clearly."),
            "D": (0, "AI awareness and skills are very low across the institution.")
        }
    },
    {
        "id": 4,
        "text": "Is there ongoing training or support for AI literacy, ethical use, and responsible adoption?",
        "dimension": "Education & Training",
        "choices": {
            "A": (3, "Yes, there is structured training and support for AI literacy."),
            "B": (2, "Some training exists but it is not comprehensive."),
            "C": (1, "Training is available only informally or on request."),
            "D": (0, "There is no training or support for AI literacy yet.")
        }
    },
    {
        "id": 5,
        "text": "Does leadership actively sponsor AI readiness initiatives and allocate resources for implementation?",
        "dimension": "Governance & Policy",
        "choices": {
            "A": (3, "Leadership is actively sponsoring AI initiatives with clear resources."),
            "B": (2, "Leadership shows some interest but resourcing is uneven."),
            "C": (1, "Leadership support is limited and not well-coordinated."),
            "D": (0, "Leadership has not yet committed resources to AI readiness.")
        }
    },
    {
        "id": 6,
        "text": "Are AI technologies integrated into workflows and systems with attention to security, privacy, and ethical risks?",
        "dimension": "Systems & Infrastructure",
        "choices": {
            "A": (3, "Yes, AI systems are integrated with strong security and privacy practices."),
            "B": (2, "Integration exists but governance or risk practices are still developing."),
            "C": (1, "AI technologies are used with inconsistent risk management."),
            "D": (0, "AI tools are used without formal security or privacy controls.")
        }
    },
    {
        "id": 7,
        "text": "Do departments share AI knowledge, coordinate projects, and involve multiple stakeholders in planning?",
        "dimension": "Culture & Skills",
        "choices": {
            "A": (3, "Yes, there is active collaboration and stakeholder involvement."),
            "B": (2, "There is some cross-unit sharing, but it is not consistent."),
            "C": (1, "Collaboration is rare and mostly informal."),
            "D": (0, "Units work in isolation with little shared AI planning.")
        }
    },
    {
        "id": 8,
        "text": "Does your institution provide role-specific guidance for students, faculty, and staff on responsible AI use?",
        "dimension": "Education & Training",
        "choices": {
            "A": (3, "Yes, there is clear, role-specific guidance for different stakeholders."),
            "B": (2, "Some guidance exists but it is broad rather than role-specific."),
            "C": (1, "Guidance is minimal and general rather than tailored."),
            "D": (0, "There is no stakeholder-specific guidance available.")
        }
    }
]

RECOMMENDATIONS = {
    "Governance & Policy": [
        "Clarify AI ethics, academic integrity, and governance policies for all stakeholders.",
        "Establish a cross-functional AI readiness committee with student, faculty, and administrative representation.",
        "Document and communicate policy expectations for AI tool use in teaching and research."
    ],
    "Systems & Infrastructure": [
        "Assess current AI tool access and prioritize investments in secure, privacy-aware platforms.",
        "Align AI system integration with existing LMS, SIS, and administrative workflows.",
        "Build a simple roadmap for infrastructure improvements and AI-supported services."
    ],
    "Culture & Skills": [
        "Offer targeted awareness sessions that explain AI potentials, limitations, and ethical concerns.",
        "Create communities of practice where stakeholders can share AI experiences and use cases.",
        "Encourage leadership messaging that emphasizes responsible AI adoption."
    ],
    "Education & Training": [
        "Develop introductory AI literacy modules for students, faculty, and staff.",
        "Provide role-specific training on AI in pedagogy, research workflows, and business processes.",
        "Build a review cycle to update training materials as AI norms and tools evolve."
    ]
}
