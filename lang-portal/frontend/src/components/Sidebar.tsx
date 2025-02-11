import Drawer from '@mui/material/Drawer'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemText from '@mui/material/ListItemText'

function Sidebar() {
  return (
    <Drawer variant="permanent" anchor="left">
      <List>
        {['Dashboard', 'Words', 'Groups', 'Activities', 'Sessions', 'Settings'].map((text) => (
          <ListItem button key={text}>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  )
}

export default Sidebar 