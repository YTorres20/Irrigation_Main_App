
def validate_input(user_input:str) -> bool: 
  user_input = user_input.strip()

  if not user_input:
      return False 
  if all(ch.isalnum() or ch == "_" or ch == "-" for ch in user_input):
      return True
  else: 
      return False
  