import framebuf

class MenuItem:
    def __init__(self, label, action=None, icon_name=None, submenu=None):
        self.label = label
        self.action = action      # A function to run when clicked
        self.icon_name = icon_name # String name of the icon
        self.submenu = submenu    # Another MenuPage object
        
        # Instantiate the Icon object once if provided
        self.icon = None
        if icon_name:
            # We import here to avoid circular dependency issues if you reorganize files
            from icon import Icon 
            self.icon = Icon(icon_name)

class MenuPage:
    def __init__(self, title, items):
        self.title = title
        self.items = items
        self.selected_index = 0
        self.view_start = 0 # For scrolling long lists

class MenuSystem:
    def __init__(self, display):
        self.display = display
        self.stack = [] # History of pages
        self.current_page = None
        
        # Layout settings
        self.line_height = 12
        self.header_height = 14
        self.visible_lines = 4 # (64px - 14px header) / 12px line

    def set_root_page(self, page):
        self.current_page = page
        self.draw()

    def navigate_down(self):
        if not self.current_page: return
        page = self.current_page
        
        if page.selected_index < len(page.items) - 1:
            page.selected_index += 1
            # Handle Scrolling
            if page.selected_index >= page.view_start + self.visible_lines:
                page.view_start += 1
            self.draw()

    def navigate_up(self):
        if not self.current_page: return
        page = self.current_page
        
        if page.selected_index > 0:
            page.selected_index -= 1
            # Handle Scrolling
            if page.selected_index < page.view_start:
                page.view_start -= 1
            self.draw()

    def select(self):
        if not self.current_page: return
        item = self.current_page.items[self.current_page.selected_index]

        if item.submenu:
            # Add current page to stack (history)
            self.stack.append(self.current_page)
            # Switch to new page
            self.current_page = item.submenu
            # Reset selection on new page usually usually good practice, 
            # or keep it saved in the object (current behavior)
            self.draw()
            
        elif item.action:
            # Execute the function
            print(f"Executing: {item.label}")
            item.action()
            # Optional: Show a "Done" popup or flash screen here

    def back(self):
        if len(self.stack) > 0:
            self.current_page = self.stack.pop()
            self.draw()

    def draw(self):
        self.display.fill(0)
        
        if not self.current_page:
            self.display.show()
            return

        page = self.current_page
        
        # 1. Draw Header
        self.display.fill_rect(0, 0, 128, self.header_height, 1)
        self.display.text(page.title, 2, 3, 0)

        # 2. Draw Items
        for i in range(self.visible_lines):
            item_index = page.view_start + i
            if item_index >= len(page.items):
                break
                
            item = page.items[item_index]
            y_pos = self.header_height + (i * self.line_height) + 1
            
            # Determine spacing based on if icon exists
            has_icon = item.icon is not None
            text_x = 16 if has_icon else 4
            
            # Draw Selection Highlight
            if item_index == page.selected_index:
                # If there is an icon, don't fill the icon area white (keep it black)
                # so the white icon remains visible.
                if has_icon:
                     self.display.fill_rect(13, y_pos, 128-13, self.line_height, 1)
                else:
                     self.display.fill_rect(0, y_pos, 128, self.line_height, 1)
                
                text_color = 0 # Text becomes Black on White background
            else:
                text_color = 1 # Text remains White on Black background

            # Draw Icon
            if has_icon:
                # Simply draw the white pixels. 
                # Because we kept the background black in the logic above, this works perfectly.
                self.display.blit(item.icon.fb, 2, y_pos + 2) 

            # Draw Label
            self.display.text(item.label, text_x, y_pos + 2, text_color)

        self.display.show()
