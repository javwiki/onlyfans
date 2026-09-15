# Design System

## Overview

The captured page is a sparse X profile-status view: a white canvas, a centered profile column, and a right-side login card. The visual language is flat, crisp, and editorial, with strong black typography, pale blue-gray dividers, and a single X blue link accent. Motion should feel precise and restrained, matching the interface rather than inventing a separate brand world.

## Colors

- **Surface**: `#FFFFFF` — full-page background.
- **Primary content**: `#0F141A` — headings, logo, and dark controls.
- **Secondary text**: `#52636F` — supporting copy and metadata.
- **Borders**: `#E4EAEC` — panel and column dividers.
- **Accent**: `#1D9BF0` — X Rules link and small highlights.
- **Muted dark**: `#000000` — QR and icon details.

## Typography

- **Primary**: TwitterChirp, weights 300–800, used throughout the interface.
- **Supporting**: Google Sans, weights 500 and 700, present in sign-in UI elements.
- **Hierarchy**: 30px / 800 status headline; 20px / 700 panel heading; 16–18px body; 16px minimum labels.

## Elevation

The page is mostly flat. Depth comes from 1px `#E4EAEC` borders, rounded login-card corners, and a very soft shadow under the QR popover. Avoid dramatic gradients or heavy shadows.

## Components

- **Profile Status Column**: narrow centered column with a back arrow, Profile title, and status message.
- **Suspension Message**: bold headline with a one-line explanation and blue Rules link.
- **Sign-in Card**: rounded white panel with stacked pill buttons and horizontal divider.
- **QR App Prompt**: small rounded popover in the lower-right corner.
- **X Mark**: simple black brand mark at the top of the profile rail.

## Do's and Don'ts

### Do's

- Keep the canvas predominantly white and spacious.
- Use TwitterChirp with high-contrast black status typography.
- Animate dividers, type, and cards with clean, short movements.
- Reserve `#1D9BF0` for meaningful links and signal accents.

### Don'ts

- Do not imply access to profile posts or private information.
- Do not add invented profile photos, bio text, follower counts, or tweets.
- Do not use dark cinematic gradients that contradict the capture.
- Do not overdecorate the sparse interface.
