#!/usr/bin/python
import subprocess

competitor_list    = 'bots.txt'
scoreboard_file    = 'scoreboard.txt'
active_competitors = []

def run_arena():
  global active_competitors

  arena = Arena()

  while True:
    # Pull in any new bot versions without restarting program
    update_bots()

    # Run matches and keep track of score
    arena.run_round(active_competitors)

    # Output scoreboard to file
    print_scoreboard(active_competitors)

def update_bots():
  global active_competitors
  global competitor_list

  fopen = open(competitor_list, 'r')

  # Repopulate from the file
  for line in fopen.readlines():
    found = False
    for gladiator in active_competitors:
      if gladiator.version == line.rstrip():
        found = True
    if found == False:
      print "A challenger appears: " + line.rstrip()
      active_competitors.append( Bot(line.rstrip()) )

  #print "Finished loading challengers: " + str(len(active_competitors)) + " are here."

  fopen.close()

def print_scoreboard(competitors):
  global scoreboard_file
  # Sort competitors by best ratio
  competitors = sorted(competitors, key=lambda k: k.wins / k.matches)

  # Output to file
  fopen = open(scoreboard_file, 'w')
  for competitor in competitors:
    fopen.write(competitor.version + ": " + str(competitor.wins) + "/" + str(competitor.matches) + " - " + str(competitor.wins / competitor.matches) + "%\n")
  fopen.close()

class Bot:
  def __init__(self, source):
    self.wins    = 0
    self.matches = 0
    self.version = source.rstrip()

class Arena:
  def run_round(self, competitor_list):
    # Play a round by pitting every bot against every other bot
    for competitor in competitor_list:
      for challenger in competitor_list:
        if competitor.version != challenger.version:
          self.run_match(competitor, challenger)

  def run_match(self, red, blue):
    #print "Scheduling a match between " + red.version + " and " + blue.version

    # Run a match between red and blue on a local server
    winner = subprocess.check_output(["perl", "play.pl", red.version, blue.version])

    #print "Winner is [" + winner + "]"
    if winner == "":
      print "No winner found between " + red.version + " and " + blue.version
      return

    red.matches += 1
    blue.matches += 1

    if (winner == red.version):
      red.wins += 1
      print red.version + " wins against " + blue.version + " (" + str(red.wins) + "/" + str(red.matches) + " wins, ratio = " + str(float(red.wins) / float(red.matches)) + ")"
    elif (winner == blue.version):
      blue.wins += 1
      print blue.version + " wins against " + red.version + " (" + str(blue.wins) + "/" + str(blue.matches) + " wins, ratio = " + str(float(blue.wins) / float(blue.matches)) + ")"
    else:
      print "No winner found between " + red.version + " and " + blue.version

print "Starting arena and waiting for competitors to be added."
run_arena()
