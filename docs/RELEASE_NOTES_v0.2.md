# ARCANA LAB v0.2 — Release notes

## Design
- Replaced rounded, panel-heavy styling with a typographic interface based on IBM Plex Sans and IBM Plex Mono.
- Added restrained element colors, fine rules, dot texture and geometric line diagrams.
- Simplified the reading output so keywords and position logic lead the experience.

## Learn
- Added an ordered 93-lesson course in eight modules.
- Added all 78 card lessons, retrieval checks and SQLite lesson completion tracking.
- Added module and overall course progress.

## Practice
- Added Single-card focus, Three-card reflection, Decision compass and Five-point compass.
- Added preview and result diagrams for every spread.
- Reorganized interpretation around position, keywords, image cue, synthesis, insight and action.

## Observe and data
- Refined charts for a restrained, consistent presentation.
- Added curriculum completion to the personal observatory and data exports.

## Verification
- 8 automated tests pass.
- The standalone SQLite setup script creates the 78-card dataset and lesson-progress table.
- Streamlit browser rendering was not end-to-end tested in the build environment because Streamlit is not installed there; the application dependencies are declared in `requirements.txt`.
