# available_skills entry for ha-bubble-dashboard
# Paste this block into the <available_skills> section of the system prompt

<skill>
<name>
ha-bubble-dashboard
</name>
<description>
Home Assistant dashboard UX and card design using Bubble Card 3.x, Streamline Card,
Sidebar Card, and the Casa5HeyneV2 merged HA/Bubble Card/Mushroom theme architecture.

TRIGGER THIS SKILL WHEN:
- Creating, designing, or improving a Lovelace dashboard or view
- Working with any Bubble Card type (pop-up, button, media-player, climate, cover,
  select, separator, calendar, sub-buttons, horizontal-buttons-stack)
- Generating or modifying a CSS theme YAML for Home Assistant
- Changing accent colours or generating a new colour palette for HA
- Changing or customising the dashboard font / typography
- Creating or modifying Streamline Card templates
- Configuring Sidebar Card or dashboard navigation
- Asking why Bubble Card or Mushroom colours don't reflect the HA theme
- Creating room pop-ups, footer nav bars, or control panels
- Wall-panel, kiosk, or fixed-display dashboard setup
- Any question about dashboard UX, layout, touch-target sizing, or accessibility
- Troubleshooting: pop-up not opening, theme not applying, Streamline template
  not found, sidebar not showing, card styling being ignored, font not loading

SYMPTOMS (Claude is going wrong without this skill):
- Hardcoding hex colours in Bubble Card YAML instead of using var() chains
- Using pre-v3.2 pop-up format (separate stack) instead of standalone cards: block
- Placing pop-ups or HBS footer inside sections: block instead of top-level cards:
- Placing pop-ups inside horizontal-stack or vertical-stack
- Using card-mod to style Bubble Cards
- Generating automations or helpers for a dashboard request
- Using a plain button card for fan, vacuum, lock, or camera entities
- Reconstructing a theme YAML from scratch instead of using the template file
- Not asking UI-mode vs YAML-mode before generating Streamline templates
- Not reminding user to clear cache after adding Streamline templates
- Generating a dashboard with masonry view instead of sections view
- Using deprecated bubble-pop-up-fix.js or referencing it
- Generating both light and dark mode without asking if display is fixed (wall panel)
- Delivering a font change without the JS loader file and configuration.yaml entry
</description>
<location>
/mnt/skills/user/ha-bubble-dashboard/SKILL.md
</location>
</skill>
