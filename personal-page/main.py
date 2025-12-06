"""
Personal Page - Built with FastHTML and MonsterUI
A modern, responsive personal website showcasing your profile, skills, and projects.
"""

from fasthtml.common import *
from monsterui.all import *

# ============================================================================
# CONFIGURATION - Customize your personal information here
# ============================================================================

PROFILE = {
    "name": "Your Name",
    "title": "Software Developer",
    "tagline": "Building beautiful things with code",
    "bio": """
        I'm a passionate developer who loves creating elegant solutions to complex problems.
        With expertise in web development, I enjoy building applications that make a difference.
        When I'm not coding, you can find me exploring new technologies and contributing to open source.
    """,
    "location": "Your City, Country",
    "email": "your.email@example.com",
    "avatar_seed": "YourName",  # Used for generating avatar - change to your name
}

SOCIAL_LINKS = [
    {"icon": "github", "url": "https://github.com/yourusername", "label": "GitHub"},
    {"icon": "linkedin", "url": "https://linkedin.com/in/yourusername", "label": "LinkedIn"},
    {"icon": "twitter", "url": "https://twitter.com/yourusername", "label": "Twitter"},
    {"icon": "mail", "url": f"mailto:{PROFILE['email']}", "label": "Email"},
]

SKILLS = [
    {"name": "Python", "level": 90},
    {"name": "JavaScript", "level": 85},
    {"name": "FastHTML", "level": 80},
    {"name": "SQL", "level": 75},
    {"name": "Docker", "level": 70},
    {"name": "Git", "level": 85},
]

PROJECTS = [
    {
        "title": "Project One",
        "description": "A cool project that does amazing things. Built with Python and FastHTML.",
        "tags": ["Python", "FastHTML", "Web"],
        "url": "https://github.com/yourusername/project-one",
    },
    {
        "title": "Project Two",
        "description": "Another awesome project showcasing my skills in data analysis.",
        "tags": ["Python", "Data Science", "ML"],
        "url": "https://github.com/yourusername/project-two",
    },
    {
        "title": "Project Three",
        "description": "A web application that solves real-world problems.",
        "tags": ["JavaScript", "React", "API"],
        "url": "https://github.com/yourusername/project-three",
    },
]

EXPERIENCES = [
    {
        "role": "Senior Developer",
        "company": "Tech Company",
        "period": "2022 - Present",
        "description": "Leading development of web applications and mentoring junior developers.",
    },
    {
        "role": "Software Developer",
        "company": "Startup Inc",
        "period": "2020 - 2022",
        "description": "Built and maintained full-stack applications using modern technologies.",
    },
    {
        "role": "Junior Developer",
        "company": "First Job Co",
        "period": "2018 - 2020",
        "description": "Started my journey in software development, learning best practices.",
    },
]

# ============================================================================
# APP SETUP
# ============================================================================

hdrs = Theme.blue.headers()
app, rt = fast_app(hdrs=hdrs)

# ============================================================================
# COMPONENTS
# ============================================================================

def SocialLinks():
    """Generate social media icon links"""
    return DivHStacked(
        *[A(UkIcon(link["icon"], height=24, width=24),
            href=link["url"],
            target="_blank",
            title=link["label"],
            cls="hover:text-primary transition-colors")
          for link in SOCIAL_LINKS],
        cls="gap-4"
    )

def SkillBar(name: str, level: int):
    """Create a skill progress bar"""
    return Div(
        DivFullySpaced(
            P(name, cls=TextT.bold),
            P(f"{level}%", cls=TextPresets.muted_sm),
        ),
        Div(
            Div(cls=f"h-2 bg-primary rounded-full", style=f"width: {level}%"),
            cls="w-full bg-secondary/20 rounded-full h-2"
        ),
        cls="mb-4"
    )

def ProjectCard(project: dict):
    """Create a project card"""
    return Card(
        H4(project["title"], cls="mb-2"),
        P(project["description"], cls=TextPresets.muted_sm + " mb-4"),
        DivHStacked(
            *[Span(tag, cls="px-2 py-1 bg-secondary/20 rounded text-xs")
              for tag in project["tags"]],
            cls="gap-2 flex-wrap"
        ),
        footer=A(
            DivLAligned(UkIcon("external-link", height=16, width=16), "View Project"),
            href=project["url"],
            target="_blank",
            cls=ButtonT.secondary + " text-sm"
        ),
        cls=CardT.hover
    )

def ExperienceItem(exp: dict):
    """Create an experience timeline item"""
    return Div(
        DivFullySpaced(
            Div(
                H4(exp["role"], cls="mb-1"),
                P(exp["company"], cls=TextPresets.muted_sm),
            ),
            Span(exp["period"], cls="text-sm text-muted-foreground"),
        ),
        P(exp["description"], cls="mt-2"),
        cls="border-l-2 border-primary pl-4 mb-6"
    )

def NavBar_():
    """Create the navigation bar"""
    return NavBar(
        A("About", href="#about"),
        A("Skills", href="#skills"),
        A("Projects", href="#projects"),
        A("Experience", href="#experience"),
        A("Contact", href="#contact"),
        brand=H3(PROFILE["name"], cls="font-bold")
    )

def HeroSection():
    """Create the hero/intro section"""
    return Section(
        Container(
            DivCentered(
                DiceBearAvatar(PROFILE["avatar_seed"], h=32, w=32),
                H1(PROFILE["name"], cls="mt-6 mb-2"),
                H3(PROFILE["title"], cls=TextPresets.muted_lg + " mb-4"),
                P(PROFILE["tagline"], cls="text-lg mb-6"),
                SocialLinks(),
                DivHStacked(
                    A("View My Work", href="#projects", cls=ButtonT.primary),
                    A("Contact Me", href="#contact", cls=ButtonT.secondary),
                    cls="gap-4 mt-8"
                ),
                cls="text-center py-20"
            )
        ),
        id="hero"
    )

def AboutSection():
    """Create the about section"""
    return Section(
        Container(
            H2("About Me", cls="text-center mb-8"),
            Grid(
                Card(
                    P(PROFILE["bio"].strip(), cls="text-lg leading-relaxed"),
                    DivHStacked(
                        UkIcon("map-pin", height=20, width=20),
                        P(PROFILE["location"]),
                        cls="gap-2 mt-4"
                    ),
                ),
                cols_lg=1
            )
        ),
        id="about",
        cls="py-16 bg-secondary/5"
    )

def SkillsSection():
    """Create the skills section"""
    return Section(
        Container(
            H2("Skills", cls="text-center mb-8"),
            Grid(
                Card(
                    *[SkillBar(skill["name"], skill["level"]) for skill in SKILLS]
                ),
                cols_lg=1
            )
        ),
        id="skills",
        cls="py-16"
    )

def ProjectsSection():
    """Create the projects section"""
    return Section(
        Container(
            H2("Projects", cls="text-center mb-8"),
            Grid(
                *[ProjectCard(project) for project in PROJECTS],
                cols_lg=3
            )
        ),
        id="projects",
        cls="py-16 bg-secondary/5"
    )

def ExperienceSection():
    """Create the experience section"""
    return Section(
        Container(
            H2("Experience", cls="text-center mb-8"),
            Card(
                *[ExperienceItem(exp) for exp in EXPERIENCES]
            )
        ),
        id="experience",
        cls="py-16"
    )

def ContactSection():
    """Create the contact section"""
    return Section(
        Container(
            H2("Get In Touch", cls="text-center mb-8"),
            Card(
                DivCentered(
                    P("I'm always open to discussing new opportunities, projects, or just having a chat!",
                      cls="text-lg text-center mb-6 max-w-xl"),
                    A(
                        DivLAligned(UkIcon("mail", height=20, width=20), f"Email Me"),
                        href=f"mailto:{PROFILE['email']}",
                        cls=ButtonT.primary + " text-lg px-8 py-3"
                    ),
                    Divider(cls="my-8 max-w-xs"),
                    P("Or find me on", cls=TextPresets.muted_sm + " mb-4"),
                    SocialLinks(),
                    cls="py-8"
                )
            )
        ),
        id="contact",
        cls="py-16 bg-secondary/5"
    )

def Footer_():
    """Create the footer"""
    return Footer(
        Container(
            DivCentered(
                P(f"© 2025 {PROFILE['name']}. Built with FastHTML & MonsterUI.",
                  cls=TextPresets.muted_sm),
                cls="py-8"
            )
        ),
        cls="border-t"
    )

# ============================================================================
# ROUTES
# ============================================================================

@rt("/")
def get():
    """Main page route"""
    return Titled(
        f"{PROFILE['name']} - {PROFILE['title']}",
        NavBar_(),
        HeroSection(),
        AboutSection(),
        SkillsSection(),
        ProjectsSection(),
        ExperienceSection(),
        ContactSection(),
        Footer_(),
    )

@rt("/api/contact")
async def post(name: str, email: str, message: str):
    """Contact form submission endpoint"""
    # In a real app, you would send an email or save to database here
    print(f"Contact form submission: {name} ({email}): {message}")
    return Card(
        H4("Thank you!"),
        P("Your message has been received. I'll get back to you soon!"),
        cls="text-center"
    )

# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    serve()
