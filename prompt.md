Build Cosmic Pinball, a single-file HTML browser game.

Everything you need is in this message. Read all of it before
writing code. The design system at the bottom is long and it is not
optional.

================================================================
MECHANICS. Build exactly this. Do not substitute or reinterpret.
================================================================

- A launcher flicks a small planet into play. The player controls
  launch angle and power.
- There are no bumpers. Gravity wells bend and slingshot the
  planet's path. The wells are the whole game.
- Glowing gates score when the planet passes through them.
- Sinking the planet into a stable orbit is the big score.
- A well swallowing the planet ends the ball.
- Input must work on touch and mouse alike. Drag to aim and set
  power, release to launch. No hover-dependent interactions, no
  keyboard requirement.

================================================================
POLISH. Yours to decide.
================================================================

Layout, scoring values, difficulty curve, feedback, sound, menus,
any flourish you think earns its place. Add faint orbital trails
behind the planet. Make it feel springy and alive.

I am scoring this build partly on whether it surprises me. If you
see a good idea I did not ask for, take it.

================================================================
DELIVERABLE. Non-negotiable.
================================================================

One .html file. Pure canvas, no dependencies, no build step. It
must run by opening the file directly in a browser, desktop or
mobile, with no local server. That means no ES modules, no fetch
calls, no external assets. Canvas scales to the viewport and
handles high-DPI screens.

Iterate as long as you like. The artifact is a single file that
opens with no setup.

No attribution anywhere in the file. The <title> must be exactly
"Cosmic Pinball". No model name, no build credit, no signature in
comments, console output, or on-screen text.

================================================================
DESIGN. Follow this design system exactly.
================================================================

# Vox OS Design System — Web Reference (Canvas Build)

> HOW TO USE THIS IN A CANVAS GAME
>
> This design system was written for HTML/CSS. You are building a
> game on a single <canvas> element, so most component contracts
> (buttons, inputs, nav items) will not apply directly. What DOES
> apply, and what you must honor:
>
> 1. The token layer below is the only source of visual truth.
>    Do not invent colors, spacing, radii, or type sizes.
> 2. Canvas does not read CSS custom properties. Declare the tokens
>    in :root for the page chrome, AND mirror the values you need
>    into a JS constant object that your canvas drawing code reads
>    from. Never hardcode a hex value inline in a fillStyle call.
> 3. Glow is stateful, never decorative. Every glow in the game must
>    map to a system state (a well's pull, a gate arming, a scoring
>    event). Ambient prettiness is a violation.
> 4. Restraint over spectacle. Void ground, one accent doing the
>    work. If a visual flourish does not communicate state,
>    hierarchy, relationship, or attention, cut it.
> 5. Typography-led. Score, state, and labels are type, not chrome.
>
> Read both sections before writing code.

---

## PART 1 — tokens.css (source of visual truth)

```css
/* Vox OS Design System Tokens
   Source of truth for all visual values.
   Architecture: primitive -> semantic -> component.
*/

:root {
  /* =========================================================
     PRIMITIVE TOKENS
     Raw values live here only.
  ========================================================= */

  /* Color: base */
  --vox-color-base-void: #050509;
  --vox-color-base-void-2: #06080f;
  --vox-color-base-ink: #090d18;
  --vox-color-base-panel: #0b1020;
  --vox-color-base-panel-2: #10172a;
  --vox-color-base-white: #ffffff;
  --vox-color-base-on-accent: #031019;

  /* Color: translucent surfaces */
  --vox-color-alpha-panel-20: rgba(8, 11, 19, 0.20);
  --vox-color-alpha-panel-40: rgba(8, 11, 19, 0.40);
  --vox-color-alpha-panel-65: rgba(7, 10, 18, 0.65);
  --vox-color-alpha-panel-80: rgba(5, 5, 16, 0.80);
  --vox-color-alpha-panel-96: rgba(5, 5, 16, 0.96);
  --vox-color-alpha-control: rgba(10, 14, 24, 0.86);
  --vox-color-alpha-control-hover: rgba(13, 20, 36, 0.92);
  --vox-color-alpha-disabled: rgba(10, 14, 24, 0.42);
  --vox-color-alpha-input: rgba(5, 5, 12, 0.94);
  --vox-color-alpha-message: rgba(3, 5, 11, 0.58);
  --vox-color-alpha-proposal: rgba(12, 7, 4, 0.34);

  /* Color: text */
  --vox-color-ink-100: rgba(236, 244, 255, 0.96);
  --vox-color-ink-200: rgba(236, 244, 255, 0.86);
  --vox-color-ink-300: rgba(236, 244, 255, 0.72);
  --vox-color-ink-400: rgba(236, 244, 255, 0.56);
  --vox-color-ink-500: rgba(236, 244, 255, 0.42);

  /* Color: borders */
  --vox-color-line-100: rgba(186, 212, 255, 0.10);
  --vox-color-line-200: rgba(186, 212, 255, 0.14);
  --vox-color-line-300: rgba(186, 212, 255, 0.22);
  --vox-color-line-400: rgba(186, 212, 255, 0.34);
  --vox-color-line-cyan: rgba(57, 217, 255, 0.42);
  --vox-color-line-orange: rgba(255, 156, 66, 0.42);
  --vox-color-line-green: rgba(57, 255, 20, 0.34);
  --vox-color-line-red: rgba(255, 91, 124, 0.42);
  --vox-color-line-cyan-hot: rgba(0, 246, 255, 0.50);
  --vox-color-line-magenta-hot: rgba(255, 0, 212, 0.50);
  --vox-color-line-purple-hot: rgba(154, 77, 255, 0.50);
  --vox-color-line-orange-hot: rgba(255, 122, 0, 0.50);

  /* Color: accents */
  --vox-color-accent-cyan-400: #7bdfff;
  --vox-color-accent-cyan-500: #39d9ff;
  --vox-color-accent-cyan-600: #00f6ff;
  --vox-color-accent-magenta-500: #ff49d5;
  --vox-color-accent-purple-500: #9f78ff;
  --vox-color-accent-orange-500: #ff9c42;
  --vox-color-accent-green-500: #39ff14;
  --vox-color-accent-red-500: #ff5b7c;
  --vox-color-accent-engineer: #22d3ee;
  --vox-color-accent-analyst: #fbbf24;
  --vox-color-accent-memory: #7c9cff;

  /* Effects */
  --vox-effect-app-bg:
    radial-gradient(circle at 5% 0%, rgba(57, 217, 255, 0.13), transparent 36%),
    radial-gradient(circle at 98% 7%, rgba(255, 73, 213, 0.12), transparent 32%),
    radial-gradient(circle at 70% 95%, rgba(159, 120, 255, 0.11), transparent 38%),
    linear-gradient(180deg, #080b14 0%, #050509 58%, #030407 100%);
  --vox-effect-grid:
    linear-gradient(rgba(186, 212, 255, 0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(186, 212, 255, 0.035) 1px, transparent 1px);
  --vox-effect-top-mask: linear-gradient(to bottom, black, transparent);
  --vox-effect-card-bg: linear-gradient(160deg, rgba(14, 18, 32, 0.72), rgba(7, 10, 18, 0.80));
  --vox-effect-console-card-bg: rgba(5, 5, 16, 0.96);
  --vox-effect-console-message-user: linear-gradient(135deg, rgba(0, 246, 255, 0.15), rgba(154, 77, 255, 0.10));
  --vox-effect-title-gradient: linear-gradient(90deg, rgba(236, 244, 255, 0.96), #39d9ff, #ff49d5, #9f78ff);
  --vox-effect-panel-ambient:
    radial-gradient(circle at 30% 20%, rgba(90, 180, 255, 0.12), transparent 56%),
    radial-gradient(circle at 70% 80%, rgba(200, 80, 255, 0.10), transparent 56%),
    rgba(5, 8, 15, 0.52);
  --vox-effect-invalid-overglow:
    0 0 0 1px rgba(57, 217, 255, 0.30),
    0 0 20px rgba(57, 217, 255, 0.45),
    0 0 44px rgba(255, 73, 213, 0.45),
    0 0 70px rgba(159, 120, 255, 0.42);
  --vox-effect-invalid-saas-bg: #f7f9fc;
  --vox-effect-invalid-saas-card: #ffffff;
  --vox-effect-invalid-saas-text: #172033;

  /* Spacing: 4px base */
  --vox-space-0: 0;
  --vox-space-1: 4px;
  --vox-space-2: 8px;
  --vox-space-3: 12px;
  --vox-space-4: 16px;
  --vox-space-5: 20px;
  --vox-space-6: 24px;
  --vox-space-8: 32px;
  --vox-space-10: 40px;
  --vox-space-12: 48px;
  --vox-space-16: 64px;
  --vox-space-20: 80px;

  /* Opacity */
  --vox-opacity-0: 0;
  --vox-opacity-1: 1;

  /* Size */
  --vox-size-page-max: 1180px;
  --vox-size-page-gutter: 36px;
  --vox-size-topbar-offset: 14px;
  --vox-size-grid-line: 42px;
  --vox-size-hero-min: 620px;
  --vox-size-orbital-min: 480px;
  --vox-size-orbital-core: 122px;
  --vox-size-node-width: 128px;
  --vox-size-node-min-height: 72px;
  --vox-size-anatomy-min: 420px;
  --vox-size-rail-width: 210px;
  --vox-size-side-width: 230px;
  --vox-size-hex-field-min: 390px;
  --vox-size-hex-width: 136px;
  --vox-size-hex-height: 122px;
  --vox-size-touch-min: 36px;
  --vox-breakpoint-mobile: 920px;

  /* Typography */
  --vox-font-family-sans: Inter, "Segoe UI", system-ui, sans-serif;
  --vox-font-family-mono: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
  --vox-font-size-meta: 11px;
  --vox-font-size-caption: 12px;
  --vox-font-size-body-compact: 13px;
  --vox-font-size-body: 14px;
  --vox-font-size-body-large: 16px;
  --vox-font-size-title: 20px;
  --vox-font-size-section: 32px;
  --vox-font-size-display: 48px;
  --vox-font-size-hero-min: 48px;
  --vox-font-size-hero-max: 104px;
  --vox-line-height-tight: 0.92;
  --vox-line-height-dense: 1.35;
  --vox-line-height-body: 1.5;
  --vox-letter-spacing-label: 0.18em;
  --vox-letter-spacing-title: 0;

  /* Border */
  --vox-border-width-0: 0;
  --vox-border-width-1: 1px;
  --vox-border-width-2: 2px;

  /* Radius */
  --vox-radius-0: 0;
  --vox-radius-1: 6px;
  --vox-radius-2: 8px;
  --vox-radius-3: 12px;
  --vox-radius-4: 16px;
  --vox-radius-5: 20px;
  --vox-radius-6: 24px;
  --vox-radius-pill: 999px;

  /* Elevation */
  --vox-shadow-0: none;
  --vox-shadow-1: 0 6px 22px rgba(0, 0, 0, 0.24);
  --vox-shadow-2: 0 12px 40px rgba(0, 0, 0, 0.32);
  --vox-shadow-3: 0 24px 80px rgba(0, 0, 0, 0.42);
  --vox-shadow-inset-1: inset 0 0 32px rgba(0, 0, 0, 0.34);
  --vox-shadow-inset-2: inset 0 0 70px rgba(0, 0, 0, 0.52);

  /* Motion */
  --vox-motion-duration-instant: 80ms;
  --vox-motion-duration-fast: 150ms;
  --vox-motion-duration-medium: 200ms;
  --vox-motion-duration-slow: 300ms;
  --vox-motion-duration-ambient: 8000ms;
  --vox-motion-duration-background-ambient: 25000ms;
  --vox-motion-duration-title-ambient: 16000ms;
  --vox-motion-duration-online-pulse: 2200ms;
  --vox-motion-ease-out: cubic-bezier(0.2, 0, 0, 1);
  --vox-motion-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --vox-motion-ease-ambient: ease-in-out;

  /* Glow */
  --vox-glow-none: none;
  --vox-glow-cyan-low: 0 0 12px rgba(57, 217, 255, 0.18);
  --vox-glow-magenta-low: 0 0 12px rgba(255, 73, 213, 0.16);
  --vox-glow-purple-low: 0 0 12px rgba(159, 120, 255, 0.16);
  --vox-glow-orange-low: 0 0 12px rgba(255, 156, 66, 0.18);
  --vox-glow-green-low: 0 0 12px rgba(57, 255, 20, 0.16);
  --vox-glow-cyan-medium:
    0 0 0 1px rgba(57, 217, 255, 0.18),
    0 0 24px rgba(57, 217, 255, 0.26);
  --vox-glow-magenta-medium:
    0 0 0 1px rgba(255, 73, 213, 0.16),
    0 0 24px rgba(255, 73, 213, 0.24);
  --vox-glow-purple-medium:
    0 0 0 1px rgba(159, 120, 255, 0.16),
    0 0 24px rgba(159, 120, 255, 0.24);
  --vox-glow-orange-medium:
    0 0 0 1px rgba(255, 156, 66, 0.18),
    0 0 24px rgba(255, 156, 66, 0.28);
  --vox-glow-orange-high:
    0 0 0 1px rgba(255, 156, 66, 0.28),
    0 0 38px rgba(255, 156, 66, 0.40);
  --vox-glow-error-high:
    0 0 0 1px rgba(255, 91, 124, 0.28),
    0 0 38px rgba(255, 91, 124, 0.40);
  --vox-glow-edge-cyan:
    0 0 10px rgba(0, 246, 255, 0.25),
    0 0 30px rgba(0, 246, 255, 0.06);
  --vox-glow-edge-magenta:
    0 0 12px rgba(255, 0, 212, 0.25),
    0 0 30px rgba(255, 0, 212, 0.07);
  --vox-glow-edge-purple:
    0 0 14px rgba(154, 77, 255, 0.25),
    0 0 30px rgba(154, 77, 255, 0.07);
  --vox-glow-edge-orange:
    0 0 12px rgba(255, 122, 0, 0.23),
    0 0 30px rgba(255, 122, 0, 0.06);
  --vox-glow-console-hover:
    0 0 20px rgba(0, 246, 255, 0.40),
    0 0 40px rgba(255, 0, 212, 0.15);

  /* =========================================================
     SEMANTIC TOKENS
     References only. No raw values.
  ========================================================= */

  --vox-color-surface-app: var(--vox-color-base-void);
  --vox-color-surface-app-alt: var(--vox-color-base-void-2);
  --vox-color-surface-panel: var(--vox-color-alpha-panel-65);
  --vox-color-surface-panel-strong: var(--vox-color-alpha-panel-96);
  --vox-color-surface-console-card: var(--vox-effect-console-card-bg);
  --vox-color-surface-control: var(--vox-color-alpha-control);
  --vox-color-surface-control-hover: var(--vox-color-alpha-control-hover);
  --vox-color-surface-disabled: var(--vox-color-alpha-disabled);
  --vox-color-surface-invalid-saas: var(--vox-effect-invalid-saas-bg);
  --vox-color-surface-invalid-saas-card: var(--vox-effect-invalid-saas-card);

  --vox-color-text-primary: var(--vox-color-ink-100);
  --vox-color-text-secondary: var(--vox-color-ink-200);
  --vox-color-text-tertiary: var(--vox-color-ink-300);
  --vox-color-text-muted: var(--vox-color-ink-400);
  --vox-color-text-disabled: var(--vox-color-ink-500);
  --vox-color-text-on-accent: var(--vox-color-base-on-accent);
  --vox-color-text-invalid-saas: var(--vox-effect-invalid-saas-text);

  --vox-color-border-muted: var(--vox-color-line-100);
  --vox-color-border-default: var(--vox-color-line-200);
  --vox-color-border-strong: var(--vox-color-line-300);
  --vox-color-border-hot: var(--vox-color-line-400);

  --vox-color-state-idle: var(--vox-color-border-default);
  --vox-color-state-hover: var(--vox-color-accent-cyan-400);
  --vox-color-state-focus: var(--vox-color-accent-cyan-500);
  --vox-color-state-active: var(--vox-color-accent-cyan-500);
  --vox-color-state-pending: var(--vox-color-accent-orange-500);
  --vox-color-state-approved: var(--vox-color-accent-green-500);
  --vox-color-state-error: var(--vox-color-accent-red-500);
  --vox-color-state-loading: var(--vox-color-accent-purple-500);

  --vox-space-layout-page-compact: var(--vox-space-4);
  --vox-space-layout-page-comfortable: var(--vox-space-6);
  --vox-space-layout-grid-compact: var(--vox-space-4);
  --vox-space-layout-grid-comfortable: var(--vox-space-6);
  --vox-space-layout-section: var(--vox-space-8);
  --vox-space-layout-rail-gap: var(--vox-space-2);

  --vox-motion-state-hover: var(--vox-motion-duration-fast);
  --vox-motion-state-focus: var(--vox-motion-duration-fast);
  --vox-motion-state-change: var(--vox-motion-duration-medium);
  --vox-motion-state-reveal: var(--vox-motion-duration-slow);
  --vox-motion-state-ambient: var(--vox-motion-duration-ambient);
  --vox-motion-dashboard-edge-cycle: var(--vox-motion-duration-ambient);
  --vox-motion-dashboard-bg-shift: var(--vox-motion-duration-background-ambient);

  --vox-motion-event-message-enter-duration: var(--vox-motion-duration-slow);
  --vox-motion-event-message-enter-ease: var(--vox-motion-ease-out);
  --vox-motion-event-agent-response-duration: var(--vox-motion-duration-medium);
  --vox-motion-event-agent-response-ease: var(--vox-motion-ease-out);
  --vox-motion-event-proposal-create-duration: var(--vox-motion-duration-medium);
  --vox-motion-event-proposal-create-ease: var(--vox-motion-ease-out);
  --vox-motion-event-proposal-approve-duration: var(--vox-motion-duration-fast);
  --vox-motion-event-proposal-approve-ease: var(--vox-motion-ease-out);
  --vox-motion-event-panel-open-duration: var(--vox-motion-duration-slow);
  --vox-motion-event-panel-open-ease: var(--vox-motion-ease-out);
  --vox-motion-event-panel-close-duration: var(--vox-motion-duration-medium);
  --vox-motion-event-panel-close-ease: var(--vox-motion-ease-in);
  --vox-motion-event-state-transition-duration: var(--vox-motion-duration-medium);
  --vox-motion-event-state-transition-ease: var(--vox-motion-ease-out);

  --vox-glow-state-idle: var(--vox-glow-none);
  --vox-glow-state-live: var(--vox-glow-cyan-low);
  --vox-glow-state-hover: var(--vox-glow-cyan-low);
  --vox-glow-state-focus: var(--vox-glow-cyan-medium);
  --vox-glow-state-active: var(--vox-glow-cyan-medium);
  --vox-glow-state-pending: var(--vox-glow-orange-medium);
  --vox-glow-state-risk: var(--vox-glow-orange-high);
  --vox-glow-state-approved: var(--vox-glow-green-low);
  --vox-glow-state-error: var(--vox-glow-error-high);
  --vox-glow-state-loading: var(--vox-glow-purple-low);
  --vox-glow-state-edge-cyan: var(--vox-glow-edge-cyan);
  --vox-glow-state-edge-magenta: var(--vox-glow-edge-magenta);
  --vox-glow-state-edge-purple: var(--vox-glow-edge-purple);
  --vox-glow-state-edge-orange: var(--vox-glow-edge-orange);
  --vox-glow-state-console-hover: var(--vox-glow-console-hover);
  --vox-glow-invalid-overglow: var(--vox-effect-invalid-overglow);

  /* =========================================================
     COMPONENT TOKENS
     References only. Strictly scoped.
  ========================================================= */

  --vox-panel-bg: var(--vox-color-surface-panel);
  --vox-panel-bg-strong: var(--vox-color-surface-panel-strong);
  --vox-panel-border: var(--vox-color-border-default);
  --vox-panel-radius: var(--vox-radius-4);
  --vox-panel-padding-compact: var(--vox-space-4);
  --vox-panel-padding-comfortable: var(--vox-space-5);
  --vox-panel-gap: var(--vox-space-4);
  --vox-panel-shadow: var(--vox-shadow-2);
  --vox-panel-glow-active: var(--vox-glow-state-active);

  --vox-console-card-bg: var(--vox-color-surface-console-card);
  --vox-console-card-border: var(--vox-color-line-cyan);
  --vox-console-card-radius: var(--vox-radius-4);
  --vox-console-card-padding: var(--vox-space-4);
  --vox-console-card-glow-a: var(--vox-glow-state-edge-cyan);
  --vox-console-card-glow-b: var(--vox-glow-state-edge-magenta);
  --vox-console-card-glow-c: var(--vox-glow-state-edge-purple);
  --vox-console-card-glow-d: var(--vox-glow-state-edge-orange);
  --vox-console-card-glow-hover: var(--vox-glow-state-console-hover);
  --vox-console-card-border-a: var(--vox-color-line-cyan-hot);
  --vox-console-card-border-b: var(--vox-color-line-magenta-hot);
  --vox-console-card-border-c: var(--vox-color-line-purple-hot);
  --vox-console-card-border-d: var(--vox-color-line-orange-hot);
  --vox-console-card-edge-duration: var(--vox-motion-dashboard-edge-cycle);
  --vox-console-card-variant-a-delay: var(--vox-space-0);
  --vox-console-card-variant-b-delay: calc(var(--vox-console-card-edge-duration) / -4);
  --vox-console-card-variant-c-delay: calc(var(--vox-console-card-edge-duration) / -2);
  --vox-console-card-variant-d-delay: calc(var(--vox-console-card-edge-duration) / -1.333);

  --vox-dashboard-grid-columns: 12;
  --vox-dashboard-grid-gap: var(--vox-space-4);
  --vox-dashboard-page-padding: var(--vox-space-4);
  --vox-dashboard-page-padding-top: var(--vox-space-20);

  --vox-button-bg: var(--vox-color-surface-control);
  --vox-button-bg-hover: var(--vox-color-surface-control-hover);
  --vox-button-border: var(--vox-color-border-default);
  --vox-button-radius: var(--vox-radius-3);
  --vox-button-radius-pill: var(--vox-radius-pill);
  --vox-button-height-compact: var(--vox-space-8);
  --vox-button-height-default: var(--vox-size-touch-min);
  --vox-button-height-icon: var(--vox-size-touch-min);
  --vox-button-padding-compact: var(--vox-space-2) var(--vox-space-3);
  --vox-button-padding-default: var(--vox-space-2) var(--vox-space-4);
  --vox-button-glow-hover: var(--vox-glow-state-hover);

  --vox-input-bg: var(--vox-color-alpha-input);
  --vox-input-border: var(--vox-color-border-default);
  --vox-input-radius: var(--vox-radius-3);
  --vox-input-height-default: var(--vox-space-10);
  --vox-input-padding: var(--vox-space-3) var(--vox-space-4);
  --vox-input-placeholder: var(--vox-color-text-disabled);

  --vox-card-bg: var(--vox-effect-card-bg);
  --vox-card-border: var(--vox-color-border-default);
  --vox-card-radius: var(--vox-radius-3);
  --vox-card-padding-compact: var(--vox-space-3);
  --vox-card-padding-comfortable: var(--vox-space-4);
  --vox-card-shadow: var(--vox-shadow-1);

  --vox-nav-item-height: var(--vox-button-height-default);
  --vox-nav-item-padding: var(--vox-space-2) var(--vox-space-3);
  --vox-nav-item-radius: var(--vox-radius-3);
  --vox-nav-item-border: var(--vox-color-border-default);
  --vox-nav-item-border-active: var(--vox-color-state-active);

  --vox-message-bg: var(--vox-color-alpha-message);
  --vox-message-border: var(--vox-color-border-default);
  --vox-message-border-active: var(--vox-color-state-active);
  --vox-message-radius: var(--vox-radius-3);
  --vox-message-padding: var(--vox-space-4);
  --vox-message-meta-font: var(--vox-font-size-meta);

  --vox-proposal-bg: var(--vox-color-alpha-proposal);
  --vox-proposal-border-pending: var(--vox-color-line-orange);
  --vox-proposal-border-approved: var(--vox-color-line-green);
  --vox-proposal-border-error: var(--vox-color-line-red);
  --vox-proposal-radius: var(--vox-radius-3);
  --vox-proposal-padding: var(--vox-space-3);

  --vox-agent-avatar-size: var(--vox-size-touch-min);
  --vox-agent-card-bg: var(--vox-card-bg);
  --vox-agent-card-border: var(--vox-card-border);
  --vox-agent-status-size: var(--vox-space-2);
  --vox-agent-accent-assistant: var(--vox-color-accent-cyan-500);
  --vox-agent-accent-engineer: var(--vox-color-accent-engineer);
  --vox-agent-accent-analyst: var(--vox-color-accent-analyst);
  --vox-agent-accent-designer: var(--vox-color-accent-purple-500);
  --vox-agent-accent-disruptor: var(--vox-color-accent-magenta-500);
  --vox-agent-accent-executor: var(--vox-color-accent-green-500);
  --vox-agent-accent-memory: var(--vox-color-accent-memory);
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --vox-motion-duration-instant: 1ms;
    --vox-motion-duration-fast: 1ms;
    --vox-motion-duration-medium: 1ms;
    --vox-motion-duration-slow: 1ms;
    --vox-motion-duration-ambient: 1ms;
  }
}
```

---

## PART 2 — Vox OS Style Guide (web)

# Vox OS Design System

Vox OS is a living command center for personal intelligence: luminous, restrained, explainable, and quietly alive.

North star: if two engineers build separate Vox OS apps, the result should feel like the same system, not the same idea.

Source of truth:

- Values: [tokens.css](C:/chroma_lab/style_docs/tokens.css)
- Valid implementation example: [vox-os-style-guide.html](C:/chroma_lab/style_docs/vox-os-style-guide.html)
- Preview: [vox-os-style-guide-preview.png](C:/chroma_lab/style_docs/vox-os-style-guide-preview.png)

## System Principle

Vox OS behaves like a living organism interface.

- Reactive: UI responds to user, agent, and system events.
- Stateful: components expose idle, live, pending, approved, error, disabled, and loading states.
- Aware: color, glow, motion, density, and layout communicate meaning.
- Explainable: side effects become proposals, gates, executions, and audit entries.

Every visible change must communicate state, hierarchy, relationship, or attention. Decoration without state meaning is invalid.

## Source Of Truth

`tokens.css` defines all values. The guide, examples, and apps consume tokens only.

Token layer rules:

- Primitive tokens may contain raw values.
- Semantic tokens must reference primitive tokens.
- Component tokens must reference primitive or semantic tokens.
- Application CSS must reference semantic or component tokens.
- Component examples must not introduce raw color, spacing, shadow, typography, radius, or motion values.

## Token Architecture

Use three layers.

### Primitive Tokens

Primitive tokens are raw values without product meaning.

Required families:

- `--vox-color-base-*`
- `--vox-color-alpha-*`
- `--vox-color-accent-*`
- `--vox-space-*`
- `--vox-size-*`
- `--vox-font-*`
- `--vox-radius-*`
- `--vox-border-width-*`
- `--vox-shadow-*`
- `--vox-motion-*`
- `--vox-glow-*`
- `--vox-effect-*`

### Semantic Tokens

Semantic tokens encode meaning.

Required families:

- `--vox-color-surface-*`
- `--vox-color-text-*`
- `--vox-color-border-*`
- `--vox-color-state-*`
- `--vox-space-layout-*`
- `--vox-motion-state-*`
- `--vox-motion-event-*`
- `--vox-glow-state-*`

### Component Tokens

Component tokens are scoped contracts for one component.

Required families:

- `--vox-panel-*`
- `--vox-button-*`
- `--vox-input-*`
- `--vox-card-*`
- `--vox-nav-*`
- `--vox-message-*`
- `--vox-proposal-*`
- `--vox-agent-*`
- `--vox-console-card-*`
- `--vox-dashboard-*`

If two components need the same new value, promote it to a semantic token instead of duplicating component tokens.

## Spacing And Layout

Spacing uses the `--vox-space-*` scale. Do not create one-off spacing.

Required layout bindings:

| Surface | Compact Token | Comfortable Token |
|---|---|---|
| Page padding | `--vox-space-layout-page-compact` | `--vox-space-layout-page-comfortable` |
| Grid gap | `--vox-space-layout-grid-compact` | `--vox-space-layout-grid-comfortable` |
| Panel padding | `--vox-panel-padding-compact` | `--vox-panel-padding-comfortable` |
| Card padding | `--vox-card-padding-compact` | `--vox-card-padding-comfortable` |
| Rail gap | `--vox-space-layout-rail-gap` | `--vox-space-layout-rail-gap` |

Layout constraints:

- Main app shell uses left rail, central work surface, and right context rail when horizontal space allows.
- Context rail contains participants, audit, proposals, selected item detail, tool state, or diagnostics.
- Cards may sit inside panels.
- Cards must not contain cards.
- If a workflow exceeds the density limits, split it into tabs, rail detail, or a separate panel.

## Density Constraints

These are enforced outcomes.

| Condition | Required Outcome |
|---|---|
| Hierarchy exceeds three levels inside one panel | Split into tabs, rail, or another panel |
| More than two accent colors appear in one component | Reduce accents or restructure the component |
| Nested cards are detected | Flatten structure; use sections, rows, or a detail rail |
| Audit content loses actor, event, timestamp, or status | Restore required metadata |
| Dense panel text drops below tokenized readable sizes | Increase density preset or split content |

Dense enterprise mode is valid only when the interface remains scannable, metadata is preserved, and all controls keep required state indicators.

## Glow System

Glow is a state language. Developers may not compose custom glow stacks. Only approved glow tokens are allowed.

Glow constraints:

- One glow token per component state.
- Multiple glow layers are allowed only when pre-defined inside a single glow token.
- Arbitrary `box-shadow` stacks are invalid outside `tokens.css`.
- Glow must represent live, hover, focus, active, pending, risk, approved, error, or loading state.
- Glow is forbidden on dense body text, disabled controls, inactive nav items, and passive decoration.

Glow mapping:

| Meaning | Token |
|---|---|
| Idle | `--vox-glow-state-idle` |
| Live | `--vox-glow-state-live` |
| Hover | `--vox-glow-state-hover` |
| Focus | `--vox-glow-state-focus` |
| Active | `--vox-glow-state-active` |
| Pending | `--vox-glow-state-pending` |
| Risk | `--vox-glow-state-risk` |
| Approved | `--vox-glow-state-approved` |
| Error | `--vox-glow-state-error` |
| Loading | `--vox-glow-state-loading` |
| Dashboard edge cycle | `--vox-console-card-glow-a/b/c/d` |

### Dashboard Edge Glow

The VoxDashboard page establishes the canonical living-edge behavior:

- Dashboard panels use `console-card` anatomy, not generic cards.
- Edges cycle subtly through cyan, magenta, purple, and orange using `--vox-console-card-edge-duration`.
- Variants `a`, `b`, `c`, and `d` use delayed starts so neighboring panels are alive together but not synchronized.
- The edge cycle is ambient system presence, not a hover or alert state.
- Hover may use `--vox-console-card-glow-hover`, but it must not replace pending, error, or approval state glows.
- The panel surface remains stable; only border and edge glow shift.

Required variant mapping:

| Variant | Delay Token | Initial Glow Token |
|---|---|---|
| `glow-variant-a` | `--vox-console-card-variant-a-delay` | `--vox-console-card-glow-a` |
| `glow-variant-b` | `--vox-console-card-variant-b-delay` | `--vox-console-card-glow-b` |
| `glow-variant-c` | `--vox-console-card-variant-c-delay` | `--vox-console-card-glow-c` |
| `glow-variant-d` | `--vox-console-card-variant-d-delay` | `--vox-console-card-glow-d` |

## Interaction State Matrix

Every interactive component must implement this matrix.

| State | Color Token | Glow Token | Motion Token | Required Non-Color Indicator |
|---|---|---|---|---|
| Idle | `--vox-color-state-idle` | `--vox-glow-state-idle` | none | label or visible affordance |
| Hover | `--vox-color-state-hover` | `--vox-glow-state-hover` | `--vox-motion-state-hover` | cursor or visual affordance |
| Focus | `--vox-color-state-focus` | `--vox-glow-state-focus` | `--vox-motion-state-focus` | visible outline |
| Active | `--vox-color-state-active` | `--vox-glow-state-active` | `--vox-motion-state-hover` | active marker or selected label |
| Pending | `--vox-color-state-pending` | `--vox-glow-state-pending` | `--vox-motion-state-change` | pending label or spinner |
| Approved | `--vox-color-state-approved` | `--vox-glow-state-approved` | `--vox-motion-state-change` | approved label or check icon |
| Error | `--vox-color-state-error` | `--vox-glow-state-error` | `--vox-motion-state-change` | error icon and label |
| Disabled | `--vox-color-text-disabled` | `--vox-glow-state-idle` | none | disabled label or tooltip |
| Loading | `--vox-color-state-loading` | `--vox-glow-state-loading` | `--vox-motion-state-reveal` | spinner, skeleton, or progress label |

## Event Motion

Motion is bound to events. Abstract animation without an event is invalid.

| Event | Motion Type | Duration Token | Easing Token |
|---|---|---|---|
| Message enter | fade plus small slide | `--vox-motion-event-message-enter-duration` | `--vox-motion-event-message-enter-ease` |
| Agent response begins | pulse status dot | `--vox-motion-event-agent-response-duration` | `--vox-motion-event-agent-response-ease` |
| Proposal creation | fade plus border emphasis | `--vox-motion-event-proposal-create-duration` | `--vox-motion-event-proposal-create-ease` |
| Proposal approval | status color transition | `--vox-motion-event-proposal-approve-duration` | `--vox-motion-event-proposal-approve-ease` |
| Panel open | fade plus slide | `--vox-motion-event-panel-open-duration` | `--vox-motion-event-panel-open-ease` |
| Panel close | fade plus slide out | `--vox-motion-event-panel-close-duration` | `--vox-motion-event-panel-close-ease` |
| State transition | color, border, and label transition | `--vox-motion-event-state-transition-duration` | `--vox-motion-event-state-transition-ease` |
| Dashboard edge cycle | ambient border/glow hue shift | `--vox-console-card-edge-duration` | `--vox-motion-ease-ambient` |

Reduced motion:

- Disable ambient drift, repeated pulse, and shimmer.
- Preserve labels, borders, icons, and state changes.
- Do not make motion the only signal.

## Component Contracts

All components consume semantic or component tokens. Accessibility requirements are part of the contract and cannot be deferred.

### Panel

Purpose: primary workflow, context rail, settings group, audit rail, or tool surface.

Anatomy:

- Container
- Optional header
- Optional section label
- Body
- Optional footer/actions

Required tokens:

- Background: `--vox-panel-bg` or `--vox-panel-bg-strong`
- Border: `--vox-panel-border`
- Radius: `--vox-panel-radius`
- Padding: `--vox-panel-padding-compact` or `--vox-panel-padding-comfortable`
- Shadow: `--vox-panel-shadow`
- Active glow: `--vox-panel-glow-active`

State behavior:

- Idle: `--vox-color-state-idle`, `--vox-glow-state-idle`.
- Focus-within: `--vox-color-state-focus`, `--vox-glow-state-focus`.
- Pending: `--vox-color-state-pending`, `--vox-glow-state-pending`, pending label.
- Error: `--vox-color-state-error`, `--vox-glow-state-error`, error icon and label.
- Disabled: muted text token, no glow, no transform.

Accessibility requirements:

- Header text uses `--vox-font-size-body` or larger.
- Metadata uses `--vox-font-size-meta` or larger.
- Body text uses `--vox-font-size-body-compact` or larger.
- Error state must include color, icon, and label. Color alone is invalid.
- Focus-within must be visible without relying on glow alone.

Valid CSS:

```css
.vox-panel {
  background: var(--vox-panel-bg);
  border: var(--vox-border-width-1) solid var(--vox-panel-border);
  border-radius: var(--vox-panel-radius);
  padding: var(--vox-panel-padding-comfortable);
  box-shadow: var(--vox-panel-shadow);
  color: var(--vox-color-text-primary);
}

.vox-panel:focus-within {
  border-color: var(--vox-color-state-focus);
  box-shadow: var(--vox-glow-state-focus);
}

.vox-panel[data-state="pending"] {
  border-color: var(--vox-color-state-pending);
  box-shadow: var(--vox-glow-state-pending);
}
```

### Console Card

Purpose: dashboard modules such as Daily Briefing, Calendar, Chat, Tasks, Memories, and other living command-center panels.

Anatomy:

- Container
- Optional icon/title row
- Body content supplied by the module
- Ambient edge state
- Optional interaction or workflow state

Required tokens:

- Background: `--vox-console-card-bg`
- Border: `--vox-console-card-border`
- Radius: `--vox-console-card-radius`
- Padding: `--vox-console-card-padding`
- Variant glows: `--vox-console-card-glow-a`, `--vox-console-card-glow-b`, `--vox-console-card-glow-c`, `--vox-console-card-glow-d`
- Variant borders: `--vox-console-card-border-a`, `--vox-console-card-border-b`, `--vox-console-card-border-c`, `--vox-console-card-border-d`
- Edge duration: `--vox-console-card-edge-duration`
- Variant delays: `--vox-console-card-variant-a-delay`, `--vox-console-card-variant-b-delay`, `--vox-console-card-variant-c-delay`, `--vox-console-card-variant-d-delay`

State behavior:

- Idle/live dashboard state uses the edge cycle.
- Hover uses `--vox-console-card-glow-hover`.
- Pending, approved, loading, and error states override the animated edge with the matching state glow token.
- The edge cycle must pause or be disabled under reduced motion.
- The surface background must not animate.

Accessibility requirements:

- Animated edge is never the only state signal.
- A title or accessible label is required for every console card.
- Reduced motion must preserve static border, labels, and state chips.
- Content text follows the same size requirements as panels.

Valid CSS:

```css
.vox-console-card {
  background: var(--vox-console-card-bg);
  border: var(--vox-border-width-1) solid var(--vox-console-card-border);
  border-radius: var(--vox-console-card-radius);
  padding: var(--vox-console-card-padding);
  animation: vox-console-edge var(--vox-console-card-edge-duration) var(--vox-motion-ease-ambient) infinite;
}

.vox-console-card.glow-variant-b {
  animation-delay: var(--vox-console-card-variant-b-delay);
}
```

### Button

Purpose: command, state change, panel open, proposal decision, or form submission.

Anatomy:

- Container
- Optional leading icon
- Label
- Optional trailing status/count

Required tokens:

- Background: `--vox-button-bg`
- Hover background: `--vox-button-bg-hover`
- Border: `--vox-button-border`
- Radius: `--vox-button-radius`
- Height: `--vox-button-height-compact`, `--vox-button-height-default`, or `--vox-button-height-icon`
- Padding: `--vox-button-padding-compact` or `--vox-button-padding-default`
- Hover glow: `--vox-button-glow-hover`

State behavior:

- Hover: `--vox-color-state-hover`, `--vox-button-glow-hover`.
- Focus: `--vox-color-state-focus`, `--vox-glow-state-focus`, visible outline.
- Active: `--vox-color-state-active`, `--vox-glow-state-active`.
- Pending: `--vox-color-state-pending`, `--vox-glow-state-pending`, spinner or pending label.
- Approved: `--vox-color-state-approved`, `--vox-glow-state-approved`, check icon or approved label.
- Error: `--vox-color-state-error`, `--vox-glow-state-error`, error icon and label.
- Disabled: no glow and no transform.

Accessibility requirements:

- Label uses `--vox-font-size-caption` or larger.
- Icon-only buttons must expose an accessible name.
- Error state must include color, icon, and label.
- Pending/loading states must prevent duplicate submission.

Valid CSS:

```css
.vox-button {
  min-height: var(--vox-button-height-default);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--vox-space-2);
  padding: var(--vox-button-padding-default);
  border: var(--vox-border-width-1) solid var(--vox-button-border);
  border-radius: var(--vox-button-radius);
  background: var(--vox-button-bg);
  color: var(--vox-color-text-primary);
  transition:
    border-color var(--vox-motion-state-hover) var(--vox-motion-ease-out),
    box-shadow var(--vox-motion-state-hover) var(--vox-motion-ease-out),
    transform var(--vox-motion-state-hover) var(--vox-motion-ease-out);
}

.vox-button:hover:not(:disabled) {
  border-color: var(--vox-color-state-hover);
  background: var(--vox-button-bg-hover);
  box-shadow: var(--vox-button-glow-hover);
}

.vox-button:focus-visible {
  outline: var(--vox-border-width-2) solid var(--vox-color-state-focus);
  outline-offset: var(--vox-space-1);
  box-shadow: var(--vox-glow-state-focus);
}
```

### Input

Required tokens:

- Background: `--vox-input-bg`
- Border: `--vox-input-border`
- Radius: `--vox-input-radius`
- Height: `--vox-input-height-default`
- Padding: `--vox-input-padding`
- Placeholder: `--vox-input-placeholder`

Accessibility requirements:

- Text uses `--vox-font-size-body-compact` or larger.
- Placeholder must not be the only label.
- Focus state must include border and outline.
- Error state must include color, icon, and label.
- Disabled state must preserve readable value text.

### Card

Required tokens:

- Background: `--vox-card-bg`
- Border: `--vox-card-border`
- Radius: `--vox-card-radius`
- Padding: `--vox-card-padding-compact` or `--vox-card-padding-comfortable`
- Shadow: `--vox-card-shadow`

Accessibility requirements:

- Cards representing actions must be keyboard reachable.
- Cards may use hover lift only when interactive.
- Body text uses `--vox-font-size-body-compact` or larger.
- Maximum accent colors per card is enforced by density constraints.

### Navigation Item

Required tokens:

- Height: `--vox-nav-item-height`
- Padding: `--vox-nav-item-padding`
- Radius: `--vox-nav-item-radius`
- Border: `--vox-nav-item-border`
- Active border: `--vox-nav-item-border-active`

Accessibility requirements:

- Active item must expose `aria-current` or equivalent.
- Disabled item must expose label or tooltip.
- Idle item must not glow.
- Focus state must be visible independent of color.

### Message Block

Anatomy:

- Metadata row
- Body
- Optional actions
- Optional proposal/tool reference

Required tokens:

- Background: `--vox-message-bg`
- Border: `--vox-message-border`
- Active border: `--vox-message-border-active`
- Radius: `--vox-message-radius`
- Padding: `--vox-message-padding`
- Metadata font: `--vox-message-meta-font`

Accessibility requirements:

- Metadata must include actor, state label, and time.
- Body text uses `--vox-font-size-body-compact` or larger.
- Error/tool-failure messages include icon and label.
- Long text must wrap; horizontal scroll is invalid for normal messages.

### Proposal Block

Anatomy:

- Status
- Title
- Capability/risk chip
- Approval requirement
- Actor
- Timestamp
- Actions

Required tokens:

- Background: `--vox-proposal-bg`
- Pending border: `--vox-proposal-border-pending`
- Approved border: `--vox-proposal-border-approved`
- Error border: `--vox-proposal-border-error`
- Radius: `--vox-proposal-radius`
- Padding: `--vox-proposal-padding`

Accessibility requirements:

- Required fields: title, status, risk, capability, actor, approval state.
- Pending state must include pending label or spinner.
- Approved state must include approved label or check icon.
- Error state must include color, icon, and label.
- Actions must be explicit: Approve, Reject, Inspect, Execute.

## Agent System

Agents are stable entities across apps.

Identity fields:

- `id`
- `displayName`
- `role`
- `provider`
- `state`
- `accent`
- `capabilities`
- `memoryScope`
- `lastActiveAt`

UI enforcement:

- Identity color must appear in a persistent element: avatar ring or identity rail.
- State color appears on status chip, state label, or state border.
- If state color overrides the outer border, identity color must remain visible in avatar ring or identity rail.
- Agent color cannot change per screen, context, route, or app.
- Maximum colors in one agent card: identity accent plus current state color.

Placement:

| Visual Element | Uses |
|---|---|
| Avatar ring | Agent identity color |
| Left identity rail | Agent identity color when avatar is absent |
| Status dot | Runtime state color |
| State chip | Runtime state color and label |
| Message border | State color, unless identity rail is the only border |

Controlled state labels:

- `IDLE`
- `OBSERVING`
- `ANALYSIS`
- `DESIGN`
- `RISK`
- `PROPOSAL`
- `AWAITING_APPROVAL`
- `EXECUTION`
- `MEMORY_RECALL`
- `BLOCKED`
- `COMPLETE`
- `ERROR`

Message metadata format:

```text
{DISPLAY_NAME} - {STATE_LABEL} - {LOCAL_TIME}
```

## Patterns

### Command Shell

Required structure:

- Topbar: identity, mode, account/system status.
- Left rail: navigation.
- Center: active workflow.
- Right rail: context, audit, participants, or proposals.

### Proposal Gate

Required structure:

- Plain-language intent.
- Required capability.
- Risk.
- Approval state.
- Actor.
- Timestamp.
- Explicit actions.
- Audit result.

### Memory Recall

Required structure:

- Subject.
- Content.
- Source or confidence when available.
- Timestamp.
- Edit/delete action states.

## Visual Do / Don't Comparisons

Examples in the HTML guide are valid implementations except for panels explicitly marked `INVALID`. Invalid examples intentionally use invalid tokens so mistakes are visible while remaining centralized in `tokens.css`.

### Over-Glow vs Correct Glow

Invalid:

- Every border glows.
- More than one glow token appears on the same component state.
- Glow does not map to state.

Valid:

- One state glow token.
- Label or icon explains the state.
- Passive components use `--vox-glow-state-idle`.

### Generic SaaS vs Vox OS

Invalid:

- Generic light dashboard structure.
- No audit/proposal/context rail.
- Product state hidden behind decorative cards.

Valid:

- Command shell structure.
- Dark glass surfaces.
- Context rail with audit/proposal data.
- State labels and controlled accent usage.

### Cluttered vs Controlled Density

Invalid:

- Nested cards.
- More than two accent colors per component.
- More than three hierarchy levels.

Valid:

- Flattened rows.
- Split rail detail.
- Metadata preserved.
- Accents reduced to identity plus state.

## System Enforcement Rules

These rules are final guardrails.

- No raw visual values outside `tokens.css`.
- No custom glow stacking.
- No uncontrolled color usage.
- No layout that breaks density limits.
- No nested cards.
- No component outside a defined contract.
- No state without a state label or non-color indicator.
- No side-effect action without proposal, gate, and audit handling.
- No agent without stable identity color and state label.
- No motion without a mapped event.
- No inaccessible icon-only control.

## Prompt-Ready Agent Brief

```text
Build in Vox OS style:
- Treat the app as a living command center for personal intelligence.
- Use tokens.css as the only source of visual values.
- Consume semantic and component tokens only; do not invent raw values.
- Every visual change must communicate state, hierarchy, relationship, or attention.
- Use the command shell pattern when the app has navigation plus context.
- Implement the full interaction state matrix.
- Use only approved glow tokens; never compose custom glow stacks.
- Bind motion to explicit events.
- Agents require stable identity color, role, state label, and message metadata.
- Side effects require proposal, gate, execution, and audit states.
- If density limits are exceeded, restructure the UI.
- Keep the interface alive but never chaotic.
```

## Sources Reviewed

Synthesized from the local and GitHub repositories centered on Vox OS:

- `beebojones/yapper`
- `beebojones/chroma`
- `beebojones/vox-os`
- `beebojones/vox-core`
- `beebojones/old-vox-os`
- `beebojones/vox-os-archive`
- `beebojones/vox-os-emergent`
- `beebojones/vox-os-emergent-edit-archive`
- `beebojones/old.chroma`
