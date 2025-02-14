import { Box, List, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import SchoolIcon from '@mui/icons-material/School';
import TranslateIcon from '@mui/icons-material/Translate';
import CategoryIcon from '@mui/icons-material/Category';
import HistoryEduIcon from '@mui/icons-material/HistoryEdu';
import SettingsIcon from '@mui/icons-material/Settings';

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Study Activities', icon: <SchoolIcon />, path: '/study-activities' },
  { text: 'Words', icon: <TranslateIcon />, path: '/words' },
  { text: 'Word Groups', icon: <CategoryIcon />, path: '/groups' },
  { text: 'Sessions', icon: <HistoryEduIcon />, path: '/sessions' },
  { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
];

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    // The sidebar itself is sticky relative to its container
    <Box sx={{ 
      position: 'sticky', 
      top: 0,
      borderRight: '1px solid',
      borderColor: 'divider',
      bgcolor: 'background.paper',
    }}>
      <List>
        {menuItems.map((item) => {
          const isSelected = location.pathname === item.path;
          
          return (
            <ListItemButton
              key={item.text}
              onClick={() => navigate(item.path)}
              selected={isSelected}
              sx={{ 
                width: '100%',
                py: 1.5,
                px: 3,
                cursor: 'pointer',
                color: 'text.primary',
                textDecoration: 'none',
                '&.Mui-selected': {
                  bgcolor: 'action.selected',
                  px: 0,
                  mx: 0,
                  '&:hover': {
                    bgcolor: 'action.selectedHover',
                  },
                  '& .MuiListItemIcon-root': {
                    color: 'primary.main',
                    ml: 3,
                  },
                  '& .MuiTypography-root': {
                    color: 'primary.main',
                    fontWeight: 500
                  }
                },
                '&:hover': {
                  bgcolor: 'action.hover',
                }
              }}
            >
              <ListItemIcon 
                sx={{ 
                  minWidth: 36,
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          );
        })}
      </List>
    </Box>
  );
}

export default Sidebar;
