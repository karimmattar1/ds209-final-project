# DS209 Final Project Plan

## Project Overview
Create a web-based, interactive visualization that presents findings and/or allows exploration of a dataset.

---

## Grade Breakdown (50% of total course grade)

| Deliverable | Weight | Points |
|-------------|--------|--------|
| Exploratory Visualization | 10% | 100 pts |
| Midterm Presentation | 10% | 100 pts |
| Usability Study | 10% | 100 pts |
| Final Presentation & Report | 20% | 100 pts |

---

## Deliverables & Requirements

### 1. Project Proposal (Not graded, but required)
**Folder:** `01_Proposal/`

**Requirements (1-2 pages max):**
- [ ] Names of students in group
- [ ] Project concept
- [ ] Target users
- [ ] Tasks users will perform with visualization
- [ ] Example insight the visualization will show
- [ ] Data source(s)
- [ ] Team charter/contract (communication, workload balance, meeting cadence)

---

### 2. Exploratory Visualization (10%)
**Folder:** `02_Exploratory_Visualization/`

**Requirements:**
- [ ] Inspect data WITHOUT visualizing first
- [ ] Write down THREE hypotheses before visualizing
- [ ] For each hypothesis:
  - [ ] Visualize relevant variables multiple ways
  - [ ] Look for correlations, clusters, outliers, patterns
  - [ ] Find evidence for/against hypothesis
  - [ ] Show at least 3 steps of refinement
  - [ ] First and last visualizations should be quite different
- [ ] Describe exploration process and changes made
- [ ] Note what worked/didn't work

**Rubric:**
| Criteria | Points |
|----------|--------|
| Good judgment in analysis of representations tried | 20 |
| Experimentation with variety of chart types | 15 |
| Refinement within individual chart types | 15 |
| Applying info from one viz to enhance another | 10 |
| Clear and reasonable hypotheses | 10 |
| Reasonable conclusion for each hypothesis | 10 |
| Describing work in enough detail to follow | 10 |
| Clear and readable writing | 10 |
| **Total** | **100** |

**Submission format:** Google doc, Observable/Colab notebook, or Tableau story

---

### 3. Midterm Presentation (10%)
**Folder:** `03_Midterm_Presentation/`

**Requirements:**
- [ ] 15-minute presentation
- [ ] Show prototype with demonstrated interactions
- [ ] Show several design iterations and explain choices
- [ ] Explain testing plan
- [ ] ALL team members must participate
- [ ] Include email address at end for peer feedback

**Tools:** Can use Keynote, PowerPoint, static drawings, or live code

---

### 4. Usability Study (10%)
**Folder:** `04_Usability_Study/`

**Requirements:**
- [ ] At least 3 test subjects PER team member
- [ ] Develop task list with good coverage of content/interactions
- [ ] Include debriefing questions
- [ ] Schedule ~30 min per participant
- [ ] Record sessions (audio or video)
- [ ] Write up notes within 24 hours
- [ ] Create prioritized list of issues using MoSCoW method

**Deliverables:**
- [ ] List of test tasks and questions
- [ ] Notes showing each member's subject interviews/responses
- [ ] Prioritized list of issues and suggested changes

**Rubric:**
| Criteria | Points |
|----------|--------|
| Appropriateness of test tasks and debriefing questions | 20 |
| Thoroughness | 20 |
| Attention to what each user does | 20 |
| Accurate prioritization | 20 |
| Strong correlation between observations and suggestions | 20 |
| **Total** | **100** |

---

### 5. Final Presentation & Report (20%)
**Folder:** `05_Final_Presentation/`

**Presentation Requirements (15 min):**
- [ ] Demonstrate visualization in action
- [ ] Show changes since midterm and explain why
- [ ] Include usability testing details and conclusions
- [ ] Show how design changed based on findings
- [ ] Address choice of tools
- [ ] ALL team members must participate

**Web Report Requirements:**
- [ ] Submit URL for final project website
- [ ] Breakdown of which group members did which tasks
- [ ] 2-3 minute video demo on YouTube
- [ ] Interactive visualization
- [ ] Explanatory text including:
  - [ ] Team member names
  - [ ] Visualization goals
  - [ ] Intended audience
  - [ ] Data source(s)

**Rubric:**
| Criteria | Points |
|----------|--------|
| Final product of appropriate form | 12 |
| Successfully solves problem or informs user | 12 |
| Explanatory text is clear | 12 |
| Showed substantial iteration | 12 |
| Visualization understandable without too much effort | 10 |
| Aesthetically pleasing | 10 |
| Included results of usability testing | 10 |
| Presented data in novel way | 8 |
| Explained choice of tools | 8 |
| Everyone in group participated | 6 |
| **Total** | **100** |

---

### 6. Website
**Folder:** `06_Website/`

**Hosting:** DigitalOcean or platform of choice

**Can include:**
- Embedded Tableau visualizations
- Observable notebooks
- D3.js visualizations
- Altair/Vega-Lite

---

## Folder Structure

```
209_Final_Project/
├── PROJECT_PLAN.md (this file)
├── 01_Proposal/
│   └── proposal.md
├── 02_Exploratory_Visualization/
│   ├── hypothesis_1/
│   ├── hypothesis_2/
│   └── hypothesis_3/
├── 03_Midterm_Presentation/
│   └── slides/
├── 04_Usability_Study/
│   ├── task_list.md
│   ├── participant_notes/
│   └── prioritized_findings.md
├── 05_Final_Presentation/
│   ├── slides/
│   └── video/
├── 06_Website/
│   ├── index.html
│   └── about.html
├── data/
│   └── (raw and processed datasets)
└── assets/
    └── (images, logos, etc.)
```

---

## Example Projects for Reference

**2023 Fall:**
- [The Impact of COVID-19 on Global Population](https://apps-fall.ischool.berkeley.edu/GlobalPopulations/)
- [Green Energy Locator](https://groups.ischool.berkeley.edu/GreenEnergyLocator/)
- [Spotify Podcast Explorer](https://people.ischool.berkeley.edu/~scaperoth/spotify-staging/)

**2023 Summer:**
- [The Guide to the Michelin Guide](https://www.the-guide-to-the-mich-guide.com/) - [Demo](https://youtu.be/y-slcyI0xz4)
- [Visualizing global vaccination trends](https://groups.ischool.berkeley.edu/VaxViz/)

---

## Notes
- Old project files preserved in: `209_Final_Project_OLD/`
- Tools covered in course: D3, Altair, Tableau
