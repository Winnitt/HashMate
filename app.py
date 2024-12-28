from flask import Flask, render_template, request
import nltk
import random

# Initialize Flask app
app = Flask(__name__)

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Function to fetch random hashtag popularity data for a given description and category
def fetch_instagram_trends(description, category):
    """
    Fetch hashtag popularity data for a given description using random generation for the category.
    """
    categories = {
        "sports": [
            "Training", "Fitness", "Game", "Match", "Championship", "Playoffs", "Workout", "Athlete", "Competition", "FitnessGoals",
            "Soccer", "Basketball", "Football", "Running", "Cycling", "Swimming", "Yoga", "Strength", "Endurance", "Performance",
            "Sportsmanship", "Teamwork", "Victory", "Marathon", "Tennis", "Golf", "Baseball", "Boxing", "Crossfit", "TrackAndField",
            "TrainingCamp", "FootballLife", "Sportscaster", "FootballFan", "BaseballFan", "SportsNews", "SportsInjury", "PersonalBest",
            "AthleticPerformance", "FitnessAddict", "WorkoutRoutine", "HealthyLiving", "Exercise", "SportEvent", "FitnessMotivation",
            "GymLife", "OutdoorSports", "SportsPhotography", "SportsNutrition", "CompetitiveEdge", "StrengthAndConditioning", "ActionSports",
            "ProAthlete", "FitnessJourney", "EnduranceTraining", "AthleteLifestyle", "MentalToughness", "FitnessInspiration", "Bodybuilding",
            "HealthyLifestyle", "OutdoorAdventure", "PlayHard", "SportsWorld", "AthleteMindset", "SportTraining", "GetFit", "ExtremeSports",
            "SportInjuryRecovery", "BasketballLife", "GolfLife", "FootballTraining", "FitnessExpert", "RunningCommunity", "WeightLifting",
            "MartialArts", "TrackAndFieldEvents", "AthleteOfTheYear", "HealthAndFitness", "SportCulture", "SportFans", "TeamSpirit",
            "VictoryLap", "AthleteInspiration", "TrackTraining", "FitnessClub", "ProSports", "SportsCenter", "SportsCommunity", "AdventureSports",
            "ActiveLifestyle", "EliteAthlete", "OutdoorFitness", "SportsRecovery", "Rugby", "Skiing", "Snowboarding", "StrengthTraining",
            "HealthGoals", "SportLife", "FitnessAddiction", "FootballTraining", "SportsAchievements", "Cardio", "WeightlossJourney"
        ],
        "lifestyle": [
            "Life", "Journey", "Vibes", "LifeGoals", "Living", "Wellness", "Mindfulness", "Motivation", "Inspiration", "SelfCare",
            "Happiness", "Productivity", "Health", "WellBeing", "PositiveVibes", "Travel", "PersonalGrowth", "GoodVibes", "WorkLifeBalance",
            "DailyRoutine", "HealthyLiving", "LoveLife", "LifeHacks", "Gratitude", "MentalHealth", "Beauty", "SelfLove", "SpiritualAwakening",
            "Peace", "Success", "SelfImprovement", "Balance", "DreamBig", "Soulmate", "RelationshipGoals", "TravelGoals", "Adventure",
            "Minimalism", "DigitalNomad", "Hygge", "SelfDiscovery", "PersonalDevelopment", "WellnessJourney", "GoodHealth", "HealthyHabits",
            "LifestyleDesign", "SuccessMindset", "HealthAndWellness", "WellnessTips", "FitFam", "LifeCoach", "MindfulLiving", "NaturalLiving",
            "HomeDecor", "OrganizedLife", "GreenLiving", "EcoFriendly", "SustainableLiving", "PositiveThinking", "LiveWell", "HappyLife",
            "HealthyMind", "SelfCareRoutine", "Empowerment", "Journaling", "BePresent", "IntentionalLiving", "PeacefulMind", "HealthyChoices",
            "InnerPeace", "Relaxation", "MentalClarity", "GratitudeJournal", "StressFreeLiving", "NomadLife", "HealthyRelationships",
            "MorningRoutine", "MindBodySoul", "LifeInBalance", "HappinessIs", "LiveTheLife", "LifeStyleBlogger", "HolisticHealth", "PersonalSuccess",
            "Positivity", "InnerStrength", "Confidence", "WellnessTips", "MindsetMatters", "MindfulParenting", "EmotionalHealing", "LuxuryLife",
            "VeganLifestyle", "HolisticLiving", "JoyfulLiving", "MotivatedLife", "TransformYourLife", "HappinessIsKey", "PositiveEnergy",
            "EmpowerYourLife", "MindfulnessMeditation", "SelfWorth", "Manifestation", "PositiveChange", "MentalWellness", "ChasingDreams"
        ],
        "real_estate": [
            "Homes", "Properties", "Market", "RealEstateInvesting", "Housing", "PropertyInvestment", "RealEstateAgent", "HouseHunting",
            "LuxuryRealEstate", "InvestmentProperties", "OpenHouse", "RealEstateTips", "HomeBuyers", "DreamHome", "RealEstateForSale",
            "HouseForSale", "PropertySearch", "RealEstateMarket", "RealEstateLife", "RealEstateExpert", "CommercialRealEstate",
            "RealEstateInvestment", "RealtorLife", "RealEstateGoals", "PropertyManagement", "RentalProperties", "HomeDesign", "ModernHomes",
            "RealEstateAdvice", "RealEstatePhotography", "RealEstateMarketing", "NewHomes", "LuxuryHomes", "RealEstateDeals",
            "PropertyListings", "RealEstateInvestors", "RealEstateBusiness", "HomeRenovations", "RealEstatePhotography", "RealEstateTips",
            "PropertyValue", "HomeImprovement", "PropertyExpert", "PropertySale", "HomesForSale", "RealEstateMarketTrends", "HomeLoans",
            "PropertyRental", "InvestmentOpportunities", "RealEstateDeals", "BuyingAHouse", "PropertyInvestmentTips", "HomeDecor",
            "HouseRenovations", "SmartHome", "RealEstateInvestingTips", "PropertySelling", "RealEstateAgents", "HouseDesign", "HomeBuyersGuide",
            "RealEstateDevelopment", "CommercialProperty", "RealEstateNews", "HomeStaging", "NewConstruction", "RealEstateOpportunities",
            "Rentals", "MortgageRates", "Foreclosure", "HouseFlipping", "RealEstateTrends", "HomeUpgrades", "HomeDecorIdeas", "LuxuryLiving",
            "RealEstateListings", "HomeAndGarden", "AffordableHousing", "FirstTimeHomeBuyer", "PropertyInvestor", "RealEstateExperts",
            "RealEstateOpportunity", "MarketTrends", "LocationLocationLocation", "RealEstateMarketAnalysis", "LandForSale", "RealEstateStrategies",
            "EcoHomes", "SustainableLiving", "InteriorDesign", "HouseShopping", "HomeSearch", "RealEstateWealth", "HomeFlipping"
        ],
        "acting": [
            "ActorLife", "OnSet", "Auditions", "ActorInspiration", "Hollywood", "ActingLife", "Filming", "CastingCall", "StageActor",
            "Theater", "ActorsOfInstagram", "FilmIndustry", "MovieSet", "FilmActor", "CastingDirector", "ActingSkills", "Monologue",
            "Drama", "FilmSet", "ActionScenes", "Filmography", "MovieStar", "ActorsLife", "CelebrityLife", "FilmLovers", "OnCamera",
            "ActorTraining", "MethodActing", "StagePerformance", "TheaterActor", "FilmProduction", "VoiceActing", "SceneStudy",
            "ScreenActing", "ActorReels", "ProfessionalActor", "Auditioning", "FilmCasting", "HollywoodActress", "CelebrityStatus",
            "FilmActing", "MovieMaking", "ActorCareer", "CastingAgency", "FilmScript", "ActorHeadshots", "MovieMakingProcess", "TheaterLife",
            "ActingCoach", "HollywoodMovies", "FilmFestival", "FilmIndustryInsider", "CelebrityLifestyle", "TVShowActor", "DramaQueen",
            "ImprovActing", "ActorsStudio", "MovieCasting", "CharacterActing", "StagePresence", "ActingTips", "FilmAndTV", "ShowBiz",
            "BehindTheScenes", "ActingClasses", "ScriptReading", "ActingTechniques", "ActingCoach", "ActorAudition", "ActorsOfTheWorld",
            "EntertainmentIndustry", "Filmmaking", "Screenwriting", "FilmProduction", "MovieBuff", "TVStar", "FilmActingClass",
            "TVShowProduction", "MovieMakingTips", "FilmSetLife", "ProfessionalActing", "MethodActor", "StagePerformance", "TVStars",
            "MovieAddicts", "DramaSeries", "AuditionTips", "ActorJourney", "VoiceOverArtist", "ScriptWriting", "CastingDirectorLife"
        ],
        "foodie": [
            "Food", "Eats", "Dishes", "FoodLovers", "Delicious", "FoodPorn", "Foodie", "Cooking", "Recipes", "Tasty", "Foodstagram",
            "HealthyEats", "VeganFood", "FoodieLife", "FoodPhotography", "FoodBloggers", "FoodLover", "FoodPornDaily", "FoodieAdventures",
            "FoodNetwork", "Yummy", "Cookbook", "Homemade", "Baking", "EatClean", "EatHealthy", "GlutenFree", "VeganRecipes", "HealthyRecipes",
            "HealthyFood", "FoodiesOfInstagram", "VeganEats", "FoodieLife", "CookingClass", "FoodLove", "CleanEating", "FoodIsLife",
            "HomeCooking", "KitchenAdventures", "FoodCrawl", "FoodJourney", "TastyBites", "FoodTrends", "Gastronomy", "FoodVibes",
            "FoodHeaven", "EatWell", "FoodieCulture", "HealthyLiving", "LocalFood", "InstaFood", "EatingOut", "BakingTime", "FoodBlogging",
            "FoodStagram", "VeganLife", "CookingTime", "TastyFood", "ChefLife", "FoodieGram", "FoodChallenge", "RecipeIdeas", "FoodLoversUnite"
        ]
    }

    if category not in categories:
        return "Invalid category"

    random_hashtags = random.sample(categories[category], 5)
    return {description: random_hashtags}


# Home route to show the form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/submit', methods=['POST'])
def submit():
    description = request.form['description']
    category = request.form['category']

    # Get the trend data
    trends = fetch_instagram_trends(description, category)

    # Return the results to display
    return render_template('result.html', trends=trends, description=description, category=category)


if __name__ == '__main__':
    app.run(debug=True)
