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
│   │       ├── LanguageSelector.tsx
│   │       └── ...
│   ├── pages/
│   │   ├── LanguageSelection/
│   │   │   ├── LanguageSelectionPage.tsx
│   │   │   └── LanguageCard.tsx
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
│   ├── context/
│   │   └── LanguageContext.tsx
│   ├── theme/
│   │   └── index.ts
│   ├── types/
│   │   └── language.ts        # Language interfaces
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
  - **context/**: Contexts and providers for global state management.
  - **theme/**: Custom Material UI theme definition.
  - **types/**: Type definitions and interfaces.
  - **App.tsx & main.tsx**: App entry points.

---

## 3. Theming & Layout

- **Material UI** default theme with:
  - **Primary** color: e.g., `#1976d2` (pleasant blue).
  - **Secondary** color: a complementary hue (like pink or purple).
  - **Dark Mode** toggle in **Settings** (using MUI's theme switch).
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
- **LastSessionCard**: Shows the user's most recent study session (activity name, group, correct vs. wrong, date).  
- **QuickStatsCard**: Overall success rate, total words studied, mastery percentage, daily streak (if implemented).  
- **Start Studying** button: Navigates to `/study-activities`.  
- **Data** from:
  - `GET /dashboard/last_study_session`
  - `GET /dashboard/quick_stats`

### 4.2 Study Activities (URL: `/study-activities`)
- Displays a **grid** or **list** of "ActivityCard" components:
  - **Launch** button flow:
    1. Shows modal/dialog for group selection
    2. On confirm, calls `POST /study_sessions` with:
       ```json
       {
         "group_id": selected_group_id,
         "study_activity_id": current_activity_id
       }
       ```
    3. On success, redirects to activity URL with new session_id
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
- Clicking a group → `/groups/:id`, listing the words in that group (similar to `/words`, but filtered) for the current language in context.
- Possibly a **Start Study Session** button to begin a session for that group.

#### Groups List Page (URL: `/groups`)
- Material UI DataGrid/Table showing groups for current language:
  - Group Name (clickable)
  - Word Count (computed from relationship)
- Features:
  - Pagination controls
  - Sorting by name or word count
  - Column headers with sort indicators
  - Filtered by current language context

#### Group Details Page (URL: `/groups/:id`)
- Header section:
  - Group name
  - Total word count
- Words table for the language in context (Material UI DataGrid) showing:
  - Script (clickable, opens word details)
  - Transliteration
  - Meaning
  - Correct Count
  - Wrong Count
- Features:
  - Pagination for words list
  - Sorting on all columns
  - Click on word script opens Word Details page
  - Start Study Session button

**Data Flow:**
1. Groups List:
   - Fetches from `GET /groups` with language_code and sort/pagination
   - Updates URL with query params for sorting/pagination
2. Group Details:
   - Fetches from `GET /groups/{id}` with word list params
   - Clicking word navigates to `/words/{id}`

**Data** from:  
- `GET /groups`
- `GET /groups/:id`

### 4.9 Study Sessions Page (URL: `/sessions`)
Material UI DataGrid/Table showing:
- Header section with:
  - Column headers with sort indicators:
    - Study Session ID (numeric)
    - Activity Name (clickable link to `/activities/:id`)
    - Group Name (clickable link to `/groups/:id`)
    - Start Time (formatted datetime)
    - Last Review Time (formatted datetime)
    - Reviews Count (number of WordReviewItems)

Features:
- Pagination controls
- Sorting by any column
- Column headers with sort indicators
- Clicking on activity/group names navigates to respective detail pages
- Time formatting using a consistent format (e.g., "Feb 16, 2024 14:30")
- Reviews count displayed as a badge or numeric indicator

### 4.10 Study Session Details Page (URL: `/sessions/:id`)
Header section showing:
- Study Session ID
- Activity Name (clickable link to `/activities/:id`)
- Group Name (clickable link to `/groups/:id`)
- Start Time (formatted datetime)
- Last Review Time (formatted datetime)
- Total Reviews Count (total WordReviewItems)

Words section showing:
- Material UI DataGrid/Table with:
  - Columns:
    - Word Script (clickable link to `/words/:id`) - opens word details in new view
    - Transliteration (if available)
    - Meaning
    - Correct Count (from WordReviewItems for this session)
    - Wrong Count (from WordReviewItems for this session)

Features:
- Pagination for words list
- Sorting by any column
- Column headers with sort indicators
- Navigation links to related entities
- Consistent time formatting
- Clear visual hierarchy between header and words list
- Loading states while fetching data
- Error handling with user-friendly messages

**Data Flow:**
1. Sessions List:
   - Fetches from `GET /study_sessions` with pagination/sorting
   - Updates URL with query params
   - Formats dates using consistent datetime formatter
   - Updates when sorting/filtering changes
2. Session Details:
   - Fetches from `GET /study_sessions/:id` with words pagination/sorting
   - Updates URL with query params for words list
   - Handles loading and error states
   - Updates word list when pagination/sorting changes

**UI Components:**
1. SessionsTable:
   - Uses Material UI DataGrid
   - Handles sorting and pagination
   - Formats dates and counts
   - Renders clickable links
2. SessionHeader:
   - Displays session metadata
   - Contains navigation links
3. WordsTable:
   - Uses Material UI DataGrid
   - Handles word list pagination
   - Shows loading states
   - Renders clickable word links

### 4.11 Study Activity Flow
#### Starting a Study Session:
1. User clicks "Launch" on an activity
2. GroupSelectionDialog opens:
   - Shows list of groups with word counts
   - Allows searching/filtering groups
   - Displays selected group's details
3. On group selection and confirmation:
   - Calls `POST /study_sessions`
   - Shows loading state during creation
   - On success, redirects to activity URL
   - On error, shows error message in dialog

#### During Study Session:
1. For each word review:
   - User interacts with word (specific to activity type)
   - On completion, calls `POST /study_sessions/{session_id}/reviews`:
     ```json
     {
       "word_id": current_word_id,
       "correct": boolean_result
     }
     ```
   - Shows success/error feedback
   - Updates progress indicators

#### UI Components:
1. GroupSelectionDialog:
   - Material UI Dialog
   - Search/filter input
   - Groups list with selection
   - Confirm/Cancel buttons
   - Loading state
2. StudyProgress:
   - Shows current word count
   - Displays success rate
   - Indicates session duration

#### Error Handling:
- Network errors during session creation
- Failed word review submissions
- Invalid group selections
- Session timeout scenarios

---

**Data** from:  
- `GET /sessions`
- `GET /sessions/:id`

### 4.6 Settings (URL: `/settings`)
- **Theme** toggle (Light / Dark / System).
- **Reset Data** button (can call an admin endpoint to re-seed the DB or clear user data).

### 4.7 Language Selection
- Initial page shown before accessing main application
- Shows list of active languages
- User must select a language to proceed
- Selected language stored in session storage
- Language selection affects all subsequent views

### 4.8 Words List Page
- Material UI DataGrid/Table component
- Columns:
  - Original script
  - Transliteration (if available)
  - English meaning
- Features:
  - Pagination controls
  - Sorting by any column
  - Current language displayed in header
  - All words filtered by selected language



## 5. Implementation Details

### 5.1 Build Setup
- **Vite**
  - Modern build tool for React applications
  - Fast development server with HMR
  - Optimized production builds
  - TypeScript support out of the box

### 5.2 API Integration
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
  - Use either MUI's built-in Table Pagination props or a custom `<Pagination>` component to handle `page`, `rowsPerPage`, etc.
- **Dark Mode**  
  - Store the theme preference in a global context or Redux store. Apply via Material UI's `<ThemeProvider>`.
- **Language Context**
  ```tsx
  // Example language context
  interface LanguageContext {
    currentLanguage: string;  // ISO code
    setLanguage: (code: string) => void;
  }
  ```
- **Route Protection**
  - Redirect to language selection if no language is selected
  - Maintain selected language in sessionStorage

---

## 6. Potential Enhancements

- **Search** bar on Words or Groups pages (e.g., `GET /words?q=...`).  
- **Localization** for UI strings (like i18n if we want multiple interface languages, distinct from the "script" field).  
- **Admin Tools** if we add roles beyond a single user scenario.

---

## 7. Summary

By following these guidelines, you'll build a **React + TypeScript + Vite** front-end that integrates cleanly with the back-end API, enabling a multi-language, trackable study experience. The UI is structured around Material UI components, with each page mapped to a specific set of REST endpoints for data retrieval and updates.
