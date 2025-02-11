# FRONT-END SPECIFICATION

This document outlines the **React + TypeScript + Vite** front-end for our multi-language language-learning portal, using **Material UI** for theming and layout. It describes the project structure, recommended components, and page-by-page details.

---

## 1. Technology Overview

- **Framework**: [React (v18+)](https://react.dev/) with [TypeScript](https://www.typescriptlang.org/)  
- **Bundler**: [Vite](https://vitejs.dev/) for a fast dev server and build process  
- **UI Library**: [Material UI (v5+)](https://mui.com/) for theming, layout, and ready-made components  
- **Routing**: [React Router (v6+)](https://reactrouter.com/) for multi-page SPA  
- **HTTP Client**: [Axios](https://axios-http.com/docs/intro) for API calls to the back end

---

## 2. Project Structure

Below is an example directory layout:

frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/                # images, icons, theme assets
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Topbar.tsx
│   │   │   └── MainLayout.tsx
│   │   └── shared/
│   │       ├── Pagination.tsx
│   │       ├── DataTable.tsx
│   │       └── ...
│   ├── pages/
│   │   ├── Dashboard/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── LastSessionCard.tsx
│   │   │   └── QuickStatsCard.tsx
│   │   ├── StudyActivities/
│   │   │   ├── ActivitiesPage.tsx
│   │   │   ├── ActivityCard.tsx
│   │   │   └── ActivityDetailPage.tsx
│   │   ├── Words/
│   │   │   ├── WordsPage.tsx
│   │   │   └── WordDetailPage.tsx
│   │   ├── Groups/
│   │   │   ├── GroupsPage.tsx
│   │   │   └── GroupDetailPage.tsx
│   │   ├── Sessions/
│   │   │   ├── SessionsPage.tsx
│   │   │   └── SessionDetailPage.tsx
│   │   └── Settings/
│   │       └── SettingsPage.tsx
│   ├── routes/
│   │   └── AppRouter.tsx
│   ├── services/
│   │   └── api.ts
│   ├── theme/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
└── tsconfig.json

### Explanation of Key Folders

- **public/**: Static files like `favicon.ico`.
- **src/**: All React source code.
  - **assets/**: Images, icons, or design assets.
  - **components/**: Reusable UI elements (e.g. layout parts, shared widgets).
  - **pages/**: Major view pages (Dashboard, Study Activities, etc.).
  - **routes/**: Central routing logic with React Router.
  - **services/**: Axios configuration or other utilities.
  - **theme/**: Custom Material UI theme definition.
  - **App.tsx & main.tsx**: App entry points.

---

## 3. Theming & Layout

- **Material UI** default theme with:
  - **Primary** color: e.g., `#1976d2` (pleasant blue).
  - **Secondary** color: a complementary hue (like pink or purple).
  - **Dark Mode** toggle in **Settings** (using MUI’s theme switch).
- **MainLayout** includes:
  - **Topbar**: The app title or logo at the top.
  - **Sidebar**: Main navigation links:
    1. Dashboard  
    2. Study Activities  
    3. Words  
    4. Groups  
    5. Sessions  
    6. Settings  

#### Example Layout Sketch

 ---------------------------------------------
| Topbar (title, optional user icon)          |
 ---------------------------------------------
| Sidebar (nav) |        Main Content         |
|              |  e.g., Dashboard, etc.       |
 ---------------------------------------------

---

## 4. Pages (Detailed)

### 4.1 Dashboard (URL: `/dashboard`)
- **LastSessionCard**: Shows the user’s most recent study session (activity name, group, correct vs. wrong, date).  
- **QuickStatsCard**: Overall success rate, total words studied, mastery percentage, daily streak (if implemented).  
- **Start Studying** button: Navigates to `/study-activities`.  
- **Data** from:
  - `GET /dashboard/last_study_session`
  - `GET /dashboard/quick_stats`

### 4.2 Study Activities (URL: `/study-activities`)
- Displays a **grid** or **list** of “ActivityCard” components:
  - **Launch** button → user picks group, calls `POST /study_sessions` to create a new session.
  - **View** button → goes to `/study-activities/:id`, showing the activity detail or history.
- **Data** from:  
  - `GET /study_activities`

### 4.3 Words (URL: `/words`)
- A table showing:
  - **script**, **transliteration**, **meaning**, **correct_count**, **wrong_count**.
- Paginated & sortable (via query params `?page=1&sort_by=script&order=asc`, etc.).
- **Data** from:  
  - `GET /words`

### 4.4 Groups (URL: `/groups`)
- Table or list of groups, each showing:
  - **name**, **words_count**.
- Clicking a group → `/groups/:id`, listing the words in that group (similar to `/words`, but filtered).
- Possibly a **Start Study Session** button to begin a session for that group.

**Data** from:  
- `GET /groups`
- `GET /groups/:id`

### 4.5 Sessions (URL: `/sessions`)
- A table of all sessions:
  - ID or date/time
  - activity name
  - group name
  - correct/wrong summary
- Clicking a session → `/sessions/:id` for detail:
  - Each **word_review_item** with word, correct/wrong, timestamp.

**Data** from:  
- `GET /sessions`
- `GET /sessions/:id`

### 4.6 Settings (URL: `/settings`)
- **Theme** toggle (Light / Dark / System).
- **Reset Data** button (can call an admin endpoint to re-seed the DB or clear user data).

---

## 5. Implementation Details

- **Axios**  
  - In `services/api.ts`, create an Axios instance:  
    ```ts
    import axios from "axios";

    export const api = axios.create({
      baseURL: "http://localhost:8000", // or environment variable
    });
    ```
- **React Router**  
  - In `AppRouter.tsx`, define your routes:
    ```tsx
    <Routes>
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/study-activities" element={<ActivitiesPage />} />
      <Route path="/study-activities/:id" element={<ActivityDetailPage />} />
      <Route path="/words" element={<WordsPage />} />
      <Route path="/groups" element={<GroupsPage />} />
      <Route path="/groups/:id" element={<GroupDetailPage />} />
      <Route path="/sessions" element={<SessionsPage />} />
      <Route path="/sessions/:id" element={<SessionDetailPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="*" element={<Navigate to="/dashboard" />} />
    </Routes>
    ```
- **Pagination**  
  - Use either MUI’s built-in Table Pagination props or a custom `<Pagination>` component to handle `page`, `rowsPerPage`, etc.
- **Dark Mode**  
  - Store the theme preference in a global context or Redux store. Apply via Material UI’s `<ThemeProvider>`.

---

## 6. Potential Enhancements

- **Search** bar on Words or Groups pages (e.g., `GET /words?q=...`).  
- **Localization** for UI strings (like i18n if we want multiple interface languages, distinct from the “script” field).  
- **Admin Tools** if we add roles beyond a single user scenario.

---

## 7. Summary

By following these guidelines, you’ll build a **React + TypeScript + Vite** front-end that integrates cleanly with the back-end API, enabling a multi-language, trackable study experience. The UI is structured around Material UI components, with each page mapped to a specific set of REST endpoints for data retrieval and updates.
