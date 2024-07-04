class Button():
     # Constructor to initialize the Button object
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image # Image of the button
		self.x_pos = pos[0] # X position of the button
		self.y_pos = pos[1] # Y position of the button
		self.font = font # Font used for the button text
		self.base_color, self.hovering_color = base_color, hovering_color # Colors for base and hovering states
		self.text_input = text_input # Text to be displayed on the button
		self.text = self.font.render(self.text_input, True, self.base_color) # Render the text with the base color
		if self.image is None: 
			self.image = self.text # If no image is provided, use the text as the image
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) # Rectangle for the button's image
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # Rectangle for the button's text
    # Method to update the button on the screen

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect) # Draw the button's image
		screen.blit(self.text, self.text_rect) # Draw the button's text
    # Method to check if the button is being clicked

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True  # Return True if the position is within the button's rectangle
		return False # Otherwise, return False
 # Method to change the color of the button's text based on the mouse position
	def changeColor(self, position): 
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color) # Change to hovering color
		else:
			self.text = self.font.render(self.text_input, True, self.base_color) # Change back to base color