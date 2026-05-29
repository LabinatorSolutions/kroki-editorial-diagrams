# Diagram Selection Guide

When deciding how to visually represent information, follow these technical principles to select the best type of diagram.

---

## 1. Selection Rules of Thumb

1.  **Prefer auto-layout engines**: Do not calculate manual coordinate points (`x`, `y`). Let engines like `d2` and `plantuml` calculate positioning so diagrams remain readable under code updates.
2.  **Avoid crowded diagrams**: Keep elements within a strict complexity budget (≤9 nodes, ≤12 connections).
3.  **Vary widths for summary layout**: When rendering supplementary context text, use 2-3 column grids with varying card widths rather than identical grids.
4.  **Use serif titles and sans-serif node text**: Enforces structural design boundaries.
5.  **Always place annotation labels on arrows**: Never use disconnected text nodes to describe arrow routes.
