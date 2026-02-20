# BRD Classification Example

## Input Fragment

> "Enable hands-free voice interaction for accessibility-conscious users while maintaining response times under 1 second to feel instantaneous."

## Analysis

### Decision Tree Traversal

**Q1: WHY?** Does this answer business justification?
✅ **YES** - Describes strategic objective (accessibility) and value proposition (hands-free interaction)

**Assignment**: **BRD**

### Factor Detection

| Factor              | Present?   | Evidence                            |
| :------------------ | :--------: | :---------------------------------- |
| Numeric metrics     | ✅         | "under 1 second"                    |
| Technology-agnostic | ✅         | No specific tech mentioned          |
| User behavior       | ✅         | "hands-free interaction"            |
| Rationale           | ✅         | "for accessibility-conscious users" |

### Validation

✅ **PASS** - Technology-agnostic language
✅ **PASS** - Measurable metric included ("< 1 second")

### Output (RST)

```rst
.. brd:: Accessibility: Hands-free voice interaction
   :id: BRD-5

.. brd:: Response time must feel instantaneous (< 1 second).
   :id: BRD-5.1
   :links: BRD-5

.. brd:: Target stakeholders: Users with mobility impairments, multitasking professionals.
   :id: BRD-5.2
   :links: BRD-5
```

### Confidence

**Score**: 0.95 (High)
**Rationale**: Clear business value statement with measurable criteria, technology-agnostic language, proper BRD characteristics