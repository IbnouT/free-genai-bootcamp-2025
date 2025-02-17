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

The dashboard provides a comprehensive overview of the user's learning progress in the selected language context.

#### Components

1. **LastSessionCard**
   - Shows details of the most recent study session
   - Displays:
     - Activity name
     - Group name (with link to group details)
     - Date of session
     - Performance metrics (correct vs. wrong counts)
   - Material UI Card with clear visual hierarchy
   - Loading state while fetching data
   - "No sessions yet" state for new users
   - **Data** from: `GET /dashboard/last-study-session`

2. **StudyProgressCard**
   - Shows progress over the last month
   - Displays:
     - Words studied count
     - Total words count (from active groups)
     - Progress percentage
   - Features:
     - Material UI LinearProgress for visual representation
     - Percentage displayed prominently
     - Tooltip explaining the calculation
   - **Data** from: `GET /dashboard/study-progress`

3. **QuickStatsCard**
   - Grid layout of key statistics
   - Displays:
     - Success rate (percentage)
     - Study sessions count
     - Active groups count
     - Study streak information
   - Features:
     - Material UI Grid with 2x2 layout
     - Each stat in its own card with icon
     - Streak displayed with calendar-style icon
     - Tooltips explaining each metric
   - **Data** from: `GET /dashboard/quick-stats`

4. **Start Studying Button**
   - Prominent CTA button
   - Navigates to `/study-activities`
   - Disabled if no groups available

#### TypeScript Interfaces

```typescript
interface LastSession {
  activity_name: string;
  date: string;
  stats: {
    correct_count: number;
    wrong_count: number;
  };
  group: {
    id: number;
    name: string;
  };
}

interface StudyProgress {
  words_studied: number;
  total_words: number;
  progress_percentage: number;
}

interface QuickStats {
  success_rate: number;
  study_sessions_count: number;
  active_groups_count: number;
  study_streak: {
    days: number;
    last_study_date: string;
  };
}
```

#### Data Flow
1. On component mount:
   - Fetch all dashboard data concurrently
   - Show loading states while fetching
   - Handle errors gracefully with error boundaries
   - Refresh data periodically (e.g., every 5 minutes)

2. Error States:
   - Network errors: Show retry button
   - No data: Show appropriate empty states
   - Loading: Show skeletons for each card

3. Language Context:
   - All API calls include current language
   - Dashboard updates when language changes
   - Clear data when switching languages

#### UI/UX Considerations
1. Loading States:
   - Skeleton loaders for each card
   - Maintain layout during loading
   - Smooth transitions when data arrives

2. Error States:
   - User-friendly error messages
   - Retry buttons where appropriate
   - Fallback UI for missing data

3. Responsive Design:
   - Cards stack on mobile
   - Maintain readability at all breakpoints
   - Touch-friendly interactions

4. Accessibility:
   - ARIA labels for statistics
   - Keyboard navigation
   - High contrast mode support
   - Screen reader friendly content

### 4.2 Study Activities

#### Study Activities List Page (URL: `/study-activities`)
- Material UI Grid layout showing activity cards
- Each **ActivityCard** component contains:
  - Activity name in header
  - Activity illustration/image
  - Activity description
  - Two buttons:
    - **Launch** button: Opens group selection dialog
    - **View** button: Opens activity details page
- Features:
  - Responsive grid layout (1-3 columns based on screen size)
  - Consistent card heights
  - Loading states while fetching activities
  - Error handling with user-friendly messages
  - Language-aware filtering (shows both universal and language-specific activities)
- **Data** from:
  - `GET /study-activities?language_code={code}`

#### Study Activity Details Page (URL: `/study-activities/{activity_id}`)
- Header section:
  - Large activity card showing:
    - Activity name (larger typography)
    - Activity illustration/image
    - Activity description
    - Launch button (opens group selection)
- Sessions section:
  - Material UI DataGrid/Table showing:
    - Study Session ID
    - Group Name (clickable link to `/groups/{group_id}`)
    - Start Time (formatted datetime)
    - Last Review Time (formatted datetime)
    - Reviews Count
  - Features:
    - Pagination controls
    - Sorting by any column (created_at, last_review_at, reviews_count)
    - Sort order controls (asc/desc)
    - Column headers with sort indicators
    - Time formatting using consistent format
    - Reviews count displayed as badge/numeric indicator
- **Data** from:
  - `GET /study-activities/{activity_id}?language_code={code}`

#### UI Components

1. **ActivityCard**:
   ```tsx
   interface ActivityCardProps {
     id: number;
     name: string;
     description: string;
     imageUrl: string;
     onLaunch: () => void;
     onView: () => void;
   }
   ```
   - Material UI Card component
   - Image displayed at top
   - Name and description in content area
   - Action buttons in card actions area

2. **GroupSelectionDialog**:
   ```tsx
   interface GroupSelectionDialogProps {
     open: boolean;
     onClose: () => void;
     onConfirm: (groupId: number) => void;
     groups: Array<{
       id: number;
       name: string;
       words_count: number;
     }>;
     loading: boolean;
   }
   ```
   - Material UI Dialog
   - List of available groups with word counts
   - Search/filter functionality
   - Loading state while fetching groups
   - Confirm/Cancel buttons

3. **SessionsTable**:
   ```tsx
   interface SessionsTableProps {
     sessions: Array<{
       id: number;
       group: {
         id: number;
         name: string;
       };
       created_at: string;
       last_review_at: string;
       reviews_count: number;
     }>;
     page: number;
     perPage: number;
     total: number;
     onPageChange: (page: number) => void;
     onSortChange: (field: string, order: 'asc' | 'desc') => void;
   }
   ```
   - Material UI DataGrid
   - Clickable group names
   - Formatted timestamps
   - Sortable columns
   - Pagination controls

#### Data Flow
1. Activities List:
   - Fetches from `GET /study-activities?language_code={code}`
   - Displays loading state while fetching
   - Renders grid of ActivityCard components
   - Handles Launch/View button clicks

2. Activity Details:
   - Fetches from `GET /study-activities/{activity_id}?language_code={code}`
   - Updates URL with query params for sessions list
   - Handles loading and error states
   - Updates sessions list when pagination/sorting changes

3. Launch Flow:
   1. User clicks Launch button
   2. Opens GroupSelectionDialog
   3. On group selection:
      - Creates new session via `POST /study-sessions`
      - Shows loading state during creation
      - On success, redirects to activity URL
      - On error, shows error message in dialog

#### Error Handling
- Network errors during data fetching
- Failed session creation
- Invalid activity or group IDs
- Session timeout scenarios
- User-friendly error messages with retry options

#### Language Context Integration
- All API calls include current language code
- Activities filtered based on language support
- Group selection filtered by language
- Session history specific to language

### 4.3 Words

#### Words List Page (URL: `/words`)
- Material UI DataGrid/Table component showing:
  - Original script
  - Transliteration (if available)
  - English meaning
  - Correct count (from review history)
  - Wrong count (from review history)
- Features:
  - Pagination controls
  - Sorting by any column (script, transliteration, meaning, correct_count, wrong_count)
  - Sort order controls (asc/desc)
  - Column headers with sort indicators
  - Current language displayed in header
  - All words filtered by selected language
  - Loading states while fetching data
  - Error handling with user-friendly messages
- **Data** from:
  - `GET /words?language_code={code}&page={page}&per_page={per_page}&sort_by={field}&order={order}`

#### Word Details Page (URL: `/words/{word_id}`)
- Header section:
  - Word in original script (large typography)
  - Transliteration (if available)
  - English meaning
  - Performance metrics:
    - Correct count
    - Wrong count
    - Success rate percentage
- Groups section:
  - List of groups containing this word
  - Each group entry shows:
    - Group name (clickable link to `/groups/{group_id}`)
    - Word count in group
  - Material UI List/Grid component
- **Data** from:
  - `GET /words/{word_id}`

#### UI Components

1. **WordsTable**:
   ```tsx
   interface WordsTableProps {
     words: Array<{
       id: number;
       script: string;
       transliteration: string | null;
       meaning: string;
       correct_count: number;
       wrong_count: number;
     }>;
     page: number;
     perPage: number;
     total: number;
     sortBy: string;
     order: 'asc' | 'desc';
     onPageChange: (page: number) => void;
     onSortChange: (field: string, order: 'asc' | 'desc') => void;
     loading: boolean;
   }
   ```
   - Material UI DataGrid
   - Sortable columns with indicators
   - Pagination controls
   - Loading state

2. **WordDetailsCard**:
   ```tsx
   interface WordDetailsProps {
     word: {
       id: number;
       script: string;
       transliteration: string | null;
       meaning: string;
       correct_count: number;
       wrong_count: number;
       groups: Array<{
         id: number;
         name: string;
         words_count: number;
       }>;
     };
     loading: boolean;
   }
   ```
   - Material UI Card
   - Performance metrics display
   - Groups list with links
   - Loading state

#### Data Flow
1. Words List:
   - Fetches from `GET /words` with query parameters
   - Updates URL with pagination/sorting params
   - Handles loading and error states
   - Updates table when filters change

2. Word Details:
   - Fetches from `GET /words/{word_id}`
   - Shows loading state while fetching
   - Displays error messages on failure
   - Updates when word ID changes

#### Error Handling
- Network errors during data fetching
- Invalid word IDs
- Missing language context
- Empty results handling
- User-friendly error messages with retry options

#### Language Context Integration
- All API calls include current language code
- Words filtered by selected language
- Performance metrics specific to language context
- Groups list filtered by language

### 4.4 Groups

#### Groups List Page (URL: `/groups`)
- Material UI DataGrid/Table showing groups for current language:
  - Group Name (clickable link to details)
  - Word Count
- Features:
  - Pagination controls
  - Sorting by name or word count
  - Sort order controls (asc/desc)
  - Column headers with sort indicators
  - Filtered by current language context
  - Loading states while fetching data
  - Error handling with user-friendly messages
- **Data** from:
  - `GET /groups?language_code={code}&page={page}&per_page={per_page}&sort_by={field}&order={order}`

#### Group Details Page (URL: `/groups/{group_id}`)
- Header section:
  - Group name (large typography)
  - Total word count
  - Start Study Session button (opens activity selection)
- Words table for the language in context:
  - Material UI DataGrid showing:
    - Script (clickable, opens word details)
    - Transliteration (if available)
    - Meaning
    - Correct Count
    - Wrong Count
  - Features:
    - Pagination for words list
    - Sorting on all columns
    - Sort order controls
    - Loading states
    - Error handling
- **Data** from:
  - `GET /groups/{group_id}?language_code={code}&page={page}&per_page={per_page}&sort_by={field}&order={order}`

#### UI Components

1. **GroupsTable**:
   ```tsx
   interface GroupsTableProps {
     groups: Array<{
       id: number;
       name: string;
       words_count: number;
     }>;
     page: number;
     perPage: number;
     total: number;
     sortBy: string;
     order: 'asc' | 'desc';
     onPageChange: (page: number) => void;
     onSortChange: (field: string, order: 'asc' | 'desc') => void;
     loading: boolean;
   }
   ```
   - Material UI DataGrid
   - Sortable columns with indicators
   - Pagination controls
   - Loading state

2. **GroupDetailsHeader**:
   ```tsx
   interface GroupDetailsHeaderProps {
     group: {
       id: number;
       name: string;
       words_count: number;
     };
     onStartStudy: () => void;
     loading: boolean;
   }
   ```
   - Material UI Card/Paper
   - Action buttons
   - Loading state

3. **GroupWordsTable**:
   ```tsx
   interface GroupWordsTableProps {
     words: Array<{
       id: number;
       script: string;
       transliteration: string | null;
       meaning: string;
       correct_count: number;
       wrong_count: number;
     }>;
     page: number;
     perPage: number;
     total: number;
     sortBy: string;
     order: 'asc' | 'desc';
     onPageChange: (page: number) => void;
     onSortChange: (field: string, order: 'asc' | 'desc') => void;
     onWordClick: (wordId: number) => void;
     loading: boolean;
   }
   ```
   - Material UI DataGrid
   - Sortable columns
   - Pagination
   - Loading state
   - Word click handler

#### Data Flow
1. Groups List:
   - Fetches from `GET /groups` with query parameters
   - Updates URL with pagination/sorting params
   - Handles loading and error states
   - Updates table when filters change

2. Group Details:
   - Fetches from `GET /groups/{group_id}` with query parameters
   - Updates URL with words list params
   - Shows loading states while fetching
   - Updates word list when pagination/sorting changes

3. Study Session Flow:
   1. User clicks "Start Study Session"
   2. Opens activity selection dialog
   3. On activity selection:
      - Creates new session via `POST /study-sessions`
      - Shows loading state during creation
      - On success, redirects to activity URL
      - On error, shows error message in dialog

#### Error Handling
- Network errors during data fetching
- Invalid group IDs
- Missing language context
- Empty results handling
- Failed session creation
- User-friendly error messages with retry options

#### Language Context Integration
- All API calls include current language code
- Groups filtered by selected language
- Words list filtered by language context
- Performance metrics specific to language

### 4.5 Study Sessions

#### Study Sessions List Page (URL: `/study-sessions`)
- Material UI DataGrid/Table showing:
  - Study Session ID
  - Activity Name (clickable link to `/study-activities/{id}`)
  - Group Name (clickable link to `/groups/{id}`)
  - Start Time (formatted datetime)
  - Last Review Time (formatted datetime)
  - Reviews Count
- Features:
  - Pagination controls
  - Sorting by any column (created_at, last_review_at, reviews_count)
  - Sort order controls (asc/desc)
  - Column headers with sort indicators
  - Time formatting using consistent format
  - Reviews count displayed as badge/numeric indicator
  - Loading states while fetching data
  - Error handling with user-friendly messages
- **Data** from:
  - `GET /study-sessions?language_code={code}&page={page}&per_page={per_page}&sort_by={field}&order={order}`

#### Study Session Details Page (URL: `/study-sessions/{session_id}`)
- Header section:
  - Study Session ID
  - Activity Name (clickable link to `/study-activities/{id}`)
  - Group Name (clickable link to `/groups/{id}`)
  - Start Time (formatted datetime)
  - Last Review Time (formatted datetime)
  - Total Reviews Count
- Words section:
  - Material UI DataGrid/Table showing:
    - Word Script (clickable link to `/words/{id}`)
    - Transliteration (if available)
    - Meaning
    - Correct Count (from this session)
    - Wrong Count (from this session)
  - Features:
    - Pagination controls
    - Sorting by any column
    - Sort order controls
    - Loading states
    - Error handling
- **Data** from:
  - `GET /study-sessions/{session_id}`

#### UI Components

1. **SessionsTable**:
   ```tsx
   interface SessionsTableProps {
     sessions: Array<{
       id: number;
       activity: {
         id: number;
         name: string;
       };
       group: {
         id: number;
         name: string;
       };
       created_at: string;
       last_review_at: string;
       reviews_count: number;
     }>;
     page: number;
     perPage: number;
     total: number;
     sortBy: string;
     order: 'asc' | 'desc';
     onPageChange: (page: number) => void;
     onSortChange: (field: string, order: 'asc' | 'desc') => void;
     loading: boolean;
   }
   ```
   - Material UI DataGrid
   - Sortable columns with indicators
   - Pagination controls
   - Loading state

2. **SessionDetailsHeader**:
   ```tsx
   interface SessionDetailsHeaderProps {
     session: {
       id: number;
       activity: {
         id: number;
         name: string;
       };
       group: {
         id: number;
         name: string;
       };
       created_at: string;
       last_review_at: string;
       reviews_count: number;
     };
     loading: boolean;
   }
   ```
   - Material UI Card/Paper
   - Formatted timestamps
   - Loading state

3. **SessionWordsTable**:
   ```tsx
   interface SessionWordsTableProps {
     words: Array<{
       id: number;
       script: string;
       transliteration: string | null;
       meaning: string;
       correct_count: number;
       wrong_count: number;
     }>;
     page: number;
     perPage: number;
     total: number;
     sortBy: string;
     order: 'asc' | 'desc';
     onPageChange: (page: number) => void;
     onSortChange: (field: string, order: 'asc' | 'desc') => void;
     onWordClick: (wordId: number) => void;
     loading: boolean;
   }
   ```
   - Material UI DataGrid
   - Sortable columns
   - Pagination
   - Loading state
   - Word click handler

#### Data Flow
1. Sessions List:
   - Fetches from `GET /study-sessions` with query parameters
   - Updates URL with pagination/sorting params
   - Handles loading and error states
   - Updates table when filters change

2. Session Details:
   - Fetches from `GET /study-sessions/{session_id}`
   - Shows loading states while fetching
   - Updates word list when pagination/sorting changes
   - Handles navigation to related entities

#### Error Handling
- Network errors during data fetching
- Invalid session IDs
- Missing language context
- Empty results handling
- User-friendly error messages with retry options

#### Language Context Integration
- All API calls include current language code
- Sessions filtered by selected language
- Word details specific to language context
- Performance metrics language-aware

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
