
# Class provided in lession, adding __sub__ overloaded operator class method
class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def to_inches(self):
        return self.feet*12 + self.inches

    def __str__(self): # Updated this method to consider foot vs feet, inch vs inches
        output_feet = f"{self.feet} feet" if self.feet != 1 else f"{self.feet} foot"
        output_inches = f"{self.inches} inches" if self.inches != 1 else f"{self.inches} inch"
        output = output_feet +', '+ output_inches
        return output

    def __add__(self, other):
        # Converting both objects' heights into inches
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches

        # Adding them up
        total_height_inches = height_A_inches + height_B_inches

        # Getting the output in feet
        output_feet = total_height_inches // 12

        # Getting the output in inches
        output_inches = total_height_inches - (output_feet * 12)

        # Returning the final output as a new Height object
        return Height(output_feet, output_inches)

    def __sub__(self, other):
        # Conversion to inches for both objects
        height_A_inches = self.to_inches()
        height_B_inches = other.to_inches()

        # Subtract :  |self - other| Since distance cannot be negative
        difference = abs(height_A_inches - height_B_inches)
        difference_feet = difference // 12
        difference_inches = difference % 12

        return Height(difference_feet, difference_inches)

    def __lt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A < height_inches_B

    def __le__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A <= height_inches_B

    def __eq__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A == height_inches_B

    def __gt__(self, other):
        height_A_inches = self.to_inches()
        height_B_inches = other.to_inches()
        return height_A_inches > height_B_inches

    def __ge__(self, other):
        height_A_inches = self.to_inches()
        height_B_inches = other.to_inches()
        return height_A_inches >= height_B_inches

    def __ne__(self, other):
        height_A_inches = self.to_inches()
        height_B_inches = other.to_inches()
        return height_A_inches != height_B_inches

#---Main------------------------------------------------------------------

# __add__ overloading test: 
person_A_height = Height(5, 10)
person_B_height = Height(4, 10)

height_sum = person_A_height + person_B_height
print("\nTotal height:", height_sum)

# __sub__ overloading test:
person_C_height = Height(5,10)
person_D_height = Height(3,9)

height_difference_pos = person_C_height - person_D_height
print(f"\n{person_C_height} - {person_D_height} = {height_difference_pos}")

height_difference_neg = person_D_height - person_C_height
print(f"{person_D_height} - {person_C_height} = {height_difference_neg}")

# Test for comparison operator overloading gt(), ge(), ne():
print(f"\nHeight(4, 6) > Height(4, 5) : {Height(4, 6) > Height(4, 5)}")
print(f"Height(4, 5) >= Height(4, 5) : {Height(4, 5) >= Height(4, 5)}")
print(f"Height(5, 9) != Height(5, 10) : {Height(5, 9) != Height(5, 10)}")