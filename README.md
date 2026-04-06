# BookLeaf Author Support & Communication Portal

## 🚀 Live Demo & Credentials
*(Add your Vercel/Railway Live URL here)*

**Admin Login:** `admin@bookleaf.com` | Password: `admin123`
**Author Login:** `john_author@bookleaf.com` | Password: `author123`

---

## ⚙️ Local Setup Instructions

### 1. Backend (Django) Setup
1. Navigate to the backend directory: `cd backend`
2. Create and activate a Virtual Environment:
   * Windows: `python -m venv venv && venv\Scripts\activate`
   * Mac/Linux: `python3 -m venv venv && source venv/bin/activate`
3. Install Python dependencies: `pip install -r requirements.txt` *(Note: requires django, djangorestframework, djangorestframework-simplejwt, django-cors-headers, python-dotenv, google-genai, pymysql)*
4. Set up Environment Variables: Create a `.env` file in the `backend/` directory and add: `GEMINI_API_KEY=your_google_ai_studio_key`
5. Ensure your local MySQL database running on XAMPP/WAMP is named `bookleaf` with user `root` (password `root`). 
6. Run migrations: `python manage.py migrate`
7. Start the server: `python manage.py runserver`

### 2. Frontend (React) Setup
1. Open a new terminal and navigate to the frontend directory: `cd frontend`
2. Install NodeJS dependencies: `npm install`
3. Start the React server: `npm start`
4. The application will automatically launch at `http://localhost:3000`.

---

## 📝 Notes & Assumptions Made

While executing this assignment, I made the following practical design assumptions to simulate a robust production environment:

1. **AI Output Fallback:** I assumed that LLM APIs can drop unexpectedly due to rate limiting. To prevent the UX from breaking, the AI parsing logic was wrapped in a hard `try/catch`. If Google Gemini fails or times out, the backend gracefully catches the exception, hardcodes a default Priority/Category, and populates the Draft Response with "AI Server Unavailable. Write manually." 
2. **"UI Only" Attachment Constraints:** The brief mentioned "UI only" for the file attachment. I implemented this via controlled React State (`useState`). The attachment successfully catches the user's uploaded local file and displays it via the browser's UI, effectively staging the `FormData` for future implementation without wasting S3 bandwidth during testing.
3. **Admin Controls over AI:** I assumed the AI might sometimes make mistakes when choosing a ticket's category or priority. To fix this, I made sure normal authors cannot edit these fields, but Admins are given special dropdown menus. This allows human operators at BookLeaf to easily click and overwrite the AI's choices, ensuring the human team always has the final say.
4. **Targeted Knowledge Base:** I actively discarded the assumption that the provided `knowledge_base.json` should be fed natively to the LLM. Assuming the author database would scale to millions of elements, injecting it entirely would cause catastrophic token expenditures. Instead, my script dynamically slices the JSON file to explicitly extract *only* the logged-in Author's targeted data payload before injecting it into the Prompt Context.

---

## 🏗 Architecture Decisions & Trade-offs

1. **Frontend (React.js):** Decided to use a clean Create React App (SPA) rather than heavily-layered Next.js SSR, as the core requirement was a deeply interactive, state-heavy dashboard. React's `useEffect` and `useState` hooks provided incredibly fast, near real-time rendering for ticket polling without unnecessary complexity.
2. **Backend (Django + DRF):** Selected for its phenomenal Model-View-Controller framework and out-of-the-box REST API capabilities. Using `ModelViewSets` provided highly robust CRUD operations, instantly bringing built-in JSON input validation and predictable 400-level error responses.
3. **Database (MySQL):** Used a relational model (MySQL) to enforce strictly normalized relationships between `Users (Authors/Admins)`, `Books`, and `Tickets`.
4. **Decoupled API Security:** Both servers are totally decoupled and communicate over HTTP. We chose **JWT (JSON Web Tokens)** via `rest_framework_simplejwt` as the authentication middleware. React holds the token securely in local storage and uses an Axios interceptor to stamp the identity into the `Authorization` header of every API call. This prevents authors from forcibly accessing admin endpoints.

---

## 🤖 AI Integration & Product Thinking (Gemini API)

The AI integration was treated as a "production-grade" feature, carefully engineered for cost, safety, and accuracy.

### 1. Cost Awareness & Token Management
Calling a massive LLM with thousands of words of context for every ticket is incredibly expensive. We implemented two strong countermeasures:
*   **User Input Truncation:** Authors frequently paste 5,000+ words of email threads or log files. Before calling the LLM, the backend string-slices the ticket description to a maximum of `1,000` characters, capping input token costs entirely while retaining all the semantic context the AI needs.
*   **Dynamic Knowledge Extraction:** Instead of injecting the entire BookLeaf Author Database into the AI Prompt context window (which creates exponential $O(N)$ token usage), the system dynamically filters the JSON to exactly match the logged-in User's email, injecting *only* that author's Book, Royalty, and Status data into the prompt. 

### 2. Prompt Engineering & Tone
The prompt strictly commands the LLM to output empathetic, solution-oriented drafts that reflect standard BookLeaf protocols (e.g. 45-day payment cycles, 5-7 day print times). 

### 3. Graceful Degradation (Error Handling)
If the Gemini API rate limits, returns a 500 error, or goes entirely offline, the application will absolutely not break. The `ai_services.py` handler intercepts the exception and safely falls back to a dictionary: `{ category: "General", priority: "Medium", draft_response: "Write manually. (AI Service unavailable)" }`. 

### 4. Human-In-The-Loop
The system strictly operates as an *assistant*, not an autonomous agent. The AI outputs the Category and Priority, but Admins retain the ability to instantly override these via inline Dropdowns. The Draft Response never sends automatically; it sits in a staging area for the Admin to edit before finalizing.

---

## 🔌 API Documentation Outline

All endpoints are protected by `JWT IsAuthenticated` permissions (except signup/login). Django safely blocks Authors from accessing Admin endpoints natively via `get_queryset()`.

### Authentication
*   `POST /api/auth/login/`: Accepts `email` & `password`. Returns JWT `access` & `refresh` tokens.
*   `POST /api/auth/register/`: Creates a new Author account.

### Tickets (Core)
*   `GET /api/tickets/`: Returns tickets. (If Author: only returns owned tickets. If Admin: returns all).
*   `POST /api/tickets/`: Authors submit a new query. *Triggers the one-shot AI Classification sequence before DB save.*
*   `PATCH /api/tickets/{id}/`: Admin endpoint to update `status`, override AI `category`/`priority`, or assign tickets (`assigned_to`).

### Messaging
*   `POST /api/messages/`: Send a real-time message to a specific ticket.
*   `POST /api/internal_notes/`: (Admin Only) Stores a private note invisible to the author.

---
