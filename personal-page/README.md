# Personal Page

A modern, responsive personal website built with **FastHTML** and **MonsterUI**.

## Features

- Responsive navigation bar
- Hero section with avatar and social links
- About me section
- Skills section with progress bars
- Projects showcase with cards
- Experience timeline
- Contact section
- Clean, modern design with Tailwind CSS styling

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python main.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5001`

## Customization

Edit the configuration section at the top of `main.py` to personalize:

- **PROFILE**: Your name, title, bio, location, and email
- **SOCIAL_LINKS**: Your social media profiles
- **SKILLS**: Your technical skills and proficiency levels
- **PROJECTS**: Your portfolio projects
- **EXPERIENCES**: Your work history

## Theme

The app uses MonsterUI's blue theme by default. You can change it by modifying:

```python
hdrs = Theme.blue.headers()
```

Available themes: `blue`, `green`, `red`, `orange`, `yellow`, `violet`, `slate`, `zinc`, `stone`, `neutral`

## Tech Stack

- [FastHTML](https://fastht.ml/) - Python web framework
- [MonsterUI](https://monsterui.answer.ai/) - UI component library
- [Tailwind CSS](https://tailwindcss.com/) - Styling (via FrankenUI)
- [Lucide Icons](https://lucide.dev/) - Icon set
