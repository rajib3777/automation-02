# Wafid Booking Form - Real Configuration Data
# ============================================

# Real countries supported by Wafid
WAFID_COUNTRIES = [
    "Algeria", "Angola", "Bangladesh", "Burundi", "Cameroon", "Chad", 
    "Egypt", "Ethiopia", "Ghana", "Guatemala", "India", "Indonesia", 
    "Jordan", "Kenya", "Lebanon", "Malawi", "Mali", "Morocco", "Nepal", 
    "Niger", "Nigeria", "Pakistan", "Panama", "Philippines", "Sierra Leone", 
    "Somalia", "Sri Lanka", "Sudan", "Syria", "Tanzania", "Thailand", 
    "Tunisia", "Turkey", "Uganda"
]

# Gulf countries you can travel to
TRAVEL_DESTINATIONS = [
    "Bahrain", "Kuwait", "Oman", "Qatar", "Saudi Arabia", "UAE", "Yemen"
]

# Major cities by country (sample - in real implementation, would have all cities)
WAFID_CITIES = {
    "Algeria": ["Algiers", "Oran", "Constantine", "Blida", "Batna"],
    "Angola": ["Luanda", "Huambo", "Lobito", "Benguela", "Kuito"],
    "Bangladesh": ["Dhaka", "Chittagong", "Khulna", "Rajshahi", "Sylhet", "Rangpur", "Comilla"],
    "Burundi": ["Bujumbura", "Gitega", "Muyinga", "Ngozi", "Ruyigi"],
    "Cameroon": ["Yaoundé", "Douala", "Bamenda", "Bafoussam", "Garoua"],
    "Chad": ["N'Djamena", "Moundou", "Sarh", "Abéché", "Kelo"],
    "Egypt": ["Cairo", "Alexandria", "Giza", "Shubra El Kheima", "Port Said", "Suez", "Luxor"],
    "Ethiopia": ["Addis Ababa", "Dire Dawa", "Mekelle", "Gondar", "Awasa", "Bahir Dar"],
    "Ghana": ["Accra", "Kumasi", "Tamale", "Sekondi-Takoradi", "Cape Coast"],
    "Guatemala": ["Guatemala City", "Mixco", "Villa Nueva", "Petapa", "San Juan Sacatepéquez"],
    "India": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Pune", "Jaipur", "Lucknow"],
    "Indonesia": ["Jakarta", "Surabaya", "Bandung", "Bekasi", "Medan", "Tangerang", "Depok"],
    "Jordan": ["Amman", "Zarqa", "Irbid", "Russeifa", "Wadi as-Sir"],
    "Kenya": ["Nairobi", "Mombasa", "Nakuru", "Eldoret", "Kisumu"],
    "Lebanon": ["Beirut", "Tripoli", "Sidon", "Tyre", "Nabatiye"],
    "Malawi": ["Lilongwe", "Blantyre", "Mzuzu", "Zomba", "Kasungu"],
    "Mali": ["Bamako", "Sikasso", "Mopti", "Koutiala", "Kayes"],
    "Morocco": ["Casablanca", "Rabat", "Fez", "Marrakech", "Agadir", "Tangier", "Meknes"],
    "Nepal": ["Kathmandu", "Pokhara", "Lalitpur", "Bharatpur", "Biratnagar"],
    "Niger": ["Niamey", "Zinder", "Maradi", "Agadez", "Tahoua"],
    "Nigeria": ["Lagos", "Kano", "Ibadan", "Abuja", "Port Harcourt", "Benin City", "Kaduna"],
    "Pakistan": ["Karachi", "Lahore", "Faisalabad", "Rawalpindi", "Gujranwala", "Peshawar", "Multan", "Islamabad"],
    "Panama": ["Panama City", "San Miguelito", "Tocumen", "David", "Arraiján"],
    "Philippines": ["Manila", "Quezon City", "Davao", "Cebu City", "Zamboanga", "Antipolo", "Pasig"],
    "Sierra Leone": ["Freetown", "Bo", "Kenema", "Koidu", "Makeni"],
    "Somalia": ["Mogadishu", "Hargeisa", "Bosaso", "Kismayo", "Merca"],
    "Sri Lanka": ["Colombo", "Dehiwala-Mount Lavinia", "Moratuwa", "Negombo", "Kandy"],
    "Sudan": ["Khartoum", "Omdurman", "Khartoum North", "Nyala", "Port Sudan"],
    "Syria": ["Damascus", "Aleppo", "Homs", "Lattakia", "Hama"],
    "Tanzania": ["Dar es Salaam", "Mwanza", "Arusha", "Dodoma", "Mbeya"],
    "Thailand": ["Bangkok", "Nonthaburi", "Pak Kret", "Hat Yai", "Chiang Mai"],
    "Tunisia": ["Tunis", "Sfax", "Sousse", "Ettadhamen", "Kairouan"],
    "Turkey": ["Istanbul", "Ankara", "Izmir", "Bursa", "Adana", "Gaziantep", "Konya"],
    "Uganda": ["Kampala", "Gulu", "Lira", "Mbarara", "Jinja"]
}

# Nationalities (matching countries)
WAFID_NATIONALITIES = [
    "Algerian", "Angolan", "Bangladeshi", "Burundian", "Cameroonian", "Chadian",
    "Egyptian", "Ethiopian", "Ghanaian", "Guatemalan", "Indian", "Indonesian",
    "Jordanian", "Kenyan", "Lebanese", "Malawian", "Malian", "Moroccan", "Nepalese",
    "Nigerien", "Nigerian", "Pakistani", "Panamanian", "Filipino", "Sierra Leonean",
    "Somali", "Sri Lankan", "Sudanese", "Syrian", "Tanzanian", "Thai",
    "Tunisian", "Turkish", "Ugandan"
]

# Visa types commonly used
VISA_TYPES = [
    "Work Visa", "Family Visa", "Visit Visa", "Student Visa", 
    "Business Visa", "Transit Visa", "Tourist Visa"
]

# Gender options
GENDER_OPTIONS = ["Male", "Female"]

# Marital status options
MARITAL_STATUS_OPTIONS = ["Single", "Married", "Divorced", "Widowed"]
