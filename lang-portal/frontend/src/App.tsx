import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box } from '@mui/material';
import { theme } from './theme';
import Topbar from './components/Topbar';
import Sidebar from './components/Sidebar';

function App({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* Unified scroll container – everything bounces together */}
      <Box
        sx={{
          height: '100vh',
          overflowY: 'auto',
          WebkitOverflowScrolling: 'touch', // for native momentum on iOS
        }}
      >
        {/* Topbar is part of the natural flow */}
        <Topbar />
        {/* Flex container for Sidebar and Main content */}
        <Box sx={{ display: 'flex' }}>
          {/* Sidebar Column:
              • We add a top margin of 64px so that its natural start is just below the Topbar.
              • We give it position: relative and a minHeight so that the sticky element has proper boundaries.
          */}
          <Box
            sx={{
              width: 240,
              position: 'relative',
              flexShrink: 0,
            }}
          >
            <Sidebar />
          </Box>
          {/* Main content */}
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              pt: 0,
              pl: 0,
              pr: 3,
              pb: 3,
            }}
          >
            {children}
          </Box>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
