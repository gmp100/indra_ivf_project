// import React, { useState } from 'react';
// import './App.css';

// function App() {
//   const [user, setUser] = useState(null); 
//   const [inputUsername, setInputUsername] = useState(''); 
//   const [inputPassword, setInputPassword] = useState(''); 
//   const [loginModalOpen, setLoginModalOpen] = useState(false); 
//   const [modalOpen, setModalOpen] = useState(false); 
//   const [selectedCategory, setSelectedCategory] = useState('');
//   const [products, setProducts] = useState([]);
//   const [selectedItem, setSelectedItem] = useState(null);
  
//   // Interactive loading and response states
//   const [isLoggingIn, setIsLoggingIn] = useState(false);
//   const [isAddingToDb, setIsAddingToDb] = useState(false);
//   const [backendResponse, setBackendResponse] = useState(null);

//   const API_URL = "http://127.0.0.1:8000/api";

//   // 1. Interactive User Login
//   const handleLogin = async (e) => {
//     if (e) e.preventDefault();
    
//     if (!inputUsername || !inputPassword) {
//       alert("⚠️ Username aur Password dono fill karein!");
//       return;
//     }

//     setIsLoggingIn(true); // Loading state ON
//     try {
//       const res = await fetch(`${API_URL}/login`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ 
//           username: inputUsername, 
//           password: inputPassword 
//         })
//       });
      
//       const data = await res.json();
      
//       if (!res.ok) {
//         throw new Error(data.detail || "Database Connection Failed (503)!");
//       }
      
//       setUser({ id: data.user_id, username: data.username });
//       setInputUsername(''); 
//       setInputPassword('');
//       setLoginModalOpen(false); 
//     } catch (err) {
//       alert(`⚠️ Login Error: ${err.message}`);
//     } finally {
//       setIsLoggingIn(false); // Loading state OFF
//     }
//   };

//   // 2. Logout
//   const handleLogout = async () => {
//     if (!user || !user.id) {
//       setUser(null);
//       return;
//     }
//     try {
//       await fetch(`${API_URL}/logout/${user.id}`, { method: "POST" });
//     } catch (err) {
//       console.error("Logout backend sync failed");
//     } finally {
//       setUser(null);
//       setModalOpen(false);
//       setSelectedItem(null);
//       setBackendResponse(null);
//     }
//   };

//   // 3. Category Select
//   const handleCardClick = async (category) => {
//     if (!user) {
//       alert("login first");
//       return;
//     }
//     setSelectedCategory(category);
//     setBackendResponse(null);
//     setSelectedItem(null); 
    
//     try {
//       const res = await fetch(`${API_URL}/products/${category}`);
//       if (!res.ok) throw new Error("Could not fetch products");
//       const data = await res.json();
//       setProducts(data);
//       setModalOpen(true);
//     } catch (err) {
//       alert("Backend se options nahi mile.");
//     }
//   };

//   // 4. Interactive Cart Saving
//   const handleAddToDb = async (productId) => {
//     if (!user || !user.id) return;
    
//     setIsAddingToDb(true); // Loading state ON
//     try {
//       const res = await fetch(`${API_URL}/cart/add`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ 
//           user_id: parseInt(user.id), 
//           product_id: parseInt(productId) 
//         })
//       });
      
//       const data = await res.json();
//       if (!res.ok) throw new Error(data.detail || "Cart addition failed");
      
//       setBackendResponse(data); 
//     } catch (err) {
//       alert(`⚠️ Add to Cart Error: ${err.message}`);
//     } finally {
//       setIsAddingToDb(false); // Loading state OFF
//     }
//   };

//   return (
//     <div>
//       {/* HEADER COMPONENT */}
//       <header className="header">
//         <h2>Indra IVF E-Com</h2>
//         <div className="auth-section">
//           {user ? (
//             <>
//               <span className="user-email">🟢 Welcome, {user.username}</span>
//               <button className="btn btn-logout" onClick={handleLogout}>Logout</button>
//             </>
//           ) : (
//             <button className="btn btn-login" onClick={() => setLoginModalOpen(true)}>Login</button>
//           )}
//         </div>
//       </header>

//       {/* MAIN UI CARDS */}
//       <div className="main-container">
//         <h1>Welcome to E-Commerce Dash</h1>
//         <p>Select a category below to explore items with auto-calculated backend discounts.</p>
        
//         <div className="card-container">
//           <div className="category-card" onClick={() => handleCardClick('cloth')}>
//             👕 Cloth
//           </div>
//           <div className="category-card" onClick={() => handleCardClick('accessory')}>
//             ⌚ Accessory
//           </div>
//         </div>
//       </div>

//       {/* 1. INTERACTIVE LOGIN POP-UP */}
//       {loginModalOpen && (
//         <div className="modal-overlay">
//           <div className="modal-content login-modal">
//             <h3>Account Login</h3>
//             <p style={{ fontSize: "0.85rem", color: "#666", marginBottom: "20px" }}>
//               Naya username daalne par automatic account create ho jayega.
//             </p>
//             <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
//               <div className="input-group">
//                 <input 
//                   type="text" 
//                   required
//                   className="auth-input-full"
//                   value={inputUsername} 
//                   onChange={(e) => setInputUsername(e.target.value)} 
//                 />
//                 <label className="floating-label">Username</label>
//               </div>
//               <div className="input-group">
//                 <input 
//                   type="password" 
//                   required
//                   className="auth-input-full"
//                   value={inputPassword} 
//                   onChange={(e) => setInputPassword(e.target.value)} 
//                 />
//                 <label className="floating-label">Password</label>
//               </div>
//               <button 
//                 type="submit" 
//                 className="btn btn-login form-submit-btn" 
//                 disabled={isLoggingIn}
//               >
//                 {isLoggingIn ? "Signing In..." : "Sign In"}
//               </button>
//               <button type="button" className="btn close-btn" onClick={() => setLoginModalOpen(false)}>Cancel</button>
//             </form>
//           </div>
//         </div>
//       )}

//       {/* 2. PRODUCTS POP-UP */}
//       {modalOpen && (
//         <div className="modal-overlay">
//           <div className="modal-content">
//             <h3>Available {selectedCategory.toUpperCase()} Items</h3>
//             <p style={{fontSize: "0.85rem", color: "#666"}}>*Row select karte hi Add+ button turn ho jayega RED</p>
            
//             <div style={{ margin: '20px 0' }}>
//               {products.length === 0 ? (
//                 <p style={{color: 'red'}}>No products found in DB.</p>
//               ) : (
//                 products.map((item) => (
//                   <div 
//                     key={item.id} 
//                     className={`modal-item ${selectedItem?.id === item.id ? 'selected' : ''}`}
//                     onClick={() => {
//                       setSelectedItem(item);
//                       setBackendResponse(null); 
//                     }}
//                   >
//                     <span style={{fontWeight: '500'}}>{item.name}</span>
//                     <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
//                       <span>₹{item.base_price}</span>
//                       <button 
//                         className={`add-btn ${selectedItem?.id === item.id ? 'red' : ''}`}
//                         disabled={isAddingToDb}
//                         onClick={(e) => {
//                           e.stopPropagation(); 
//                           if (selectedItem?.id === item.id) {
//                             handleAddToDb(item.id);
//                           } else {
//                             alert("Pehle is row par click karke item select karein!");
//                           }
//                         }}
//                       >
//                         {isAddingToDb && selectedItem?.id === item.id ? "Saving..." : "Add+"}
//                       </button>
//                     </div>
//                   </div>
//                 ))
//               )}
//             </div>

//             {/* BACKEND CALCULATED RESPONSE ANIMATION BOX */}
//             {backendResponse && (
//               <div className="db-response-box fade-in-effect">
//                 <p style={{ color: '#1b5e20', fontWeight: 'bold' }}>✓ {backendResponse.message}</p>
//                 <p>Base Price: <del>₹{backendResponse.original_price}</del></p>
//                 <p>Discount Applied: <b style={{color: '#d32f2f'}}>{backendResponse.discount_applied}</b></p>
//                 <p>Final Saved DB Price: <b style={{fontSize: '1.1rem'}}>₹{backendResponse.final_price}</b></p>
//               </div>
//             )}

//             <button className="btn close-btn" onClick={() => setModalOpen(false)}>Close</button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

import React, { useState } from 'react';
import './App.css';

function App() {
  const [user, setUser] = useState(null); 
  const [inputUsername, setInputUsername] = useState(''); 
  const [inputPassword, setInputPassword] = useState(''); 
  const [loginModalOpen, setLoginModalOpen] = useState(false); 
  const [modalOpen, setModalOpen] = useState(false); 
  const [selectedCategory, setSelectedCategory] = useState('');
  const [products, setProducts] = useState([]);
  
  // Track array of multiple selected items IDs
  const [selectedItemIds, setSelectedItemIds] = useState([]);
  
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isProcessingCart, setIsProcessingCart] = useState(false);
  const [backendResponse, setBackendResponse] = useState(null);

  const API_URL = "http://127.0.0.1:8000/api";

  const handleLogin = async (e) => {
    if (e) e.preventDefault();
    if (!inputUsername || !inputPassword) return;
    setIsLoggingIn(true);
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: inputUsername, password: inputPassword })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      setUser({ id: data.user_id, username: data.username });
      setLoginModalOpen(false);
    } catch (err) { alert(err.message); }
    finally { setIsLoggingIn(false); }
  };

  const handleLogout = () => {
    setUser(null); setModalOpen(false); setSelectedItemIds([]); setBackendResponse(null);
  };

  const handleCardClick = async (category) => {
    if (!user) { alert("login first"); return; }
    setSelectedCategory(category);
    setBackendResponse(null);
    setSelectedItemIds([]); // Clear selection array on click
    try {
      const res = await fetch(`${API_URL}/products/${category}`);
      const data = await res.json();
      setProducts(data);
      setModalOpen(true);
    } catch (err) { alert("Backend synchronization loss."); }
  };

  // Multiple Row selection control toggler
  const toggleItemSelection = (id) => {
    setBackendResponse(null);
    if (selectedItemIds.includes(id)) {
      setSelectedItemIds(selectedItemIds.filter(itemId => itemId !== id));
    } else {
      setSelectedItemIds([...selectedItemIds, id]);
    }
  };

  // Submit absolute selections matrix to DB
  const handleBulkCheckout = async () => {
    if (selectedItemIds.length === 0) {
      alert("click on row");
      return;
    }
    setIsProcessingCart(true);
    try {
      const res = await fetch(`${API_URL}/cart/add-bulk`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: parseInt(user.id),
          product_ids: selectedItemIds
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      setBackendResponse(data);
    } catch (err) { alert(err.message); }
    finally { setIsProcessingCart(false); }
  };

  return (
    <div>
      <header className="header">
        <h2>Indra IVF E-Com</h2>
        <div className="auth-section">
          {user ? (
            <>
              <span className="user-email">🟢 Welcome, {user.username}</span>
              <button className="btn btn-logout" onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <button className="btn btn-login" onClick={() => setLoginModalOpen(true)}>Login</button>
          )}
        </div>
      </header>

      <div className="main-container">
        <h1>Dynamic Bulk Pricing Engine</h1>
        <div className="card-container">
          <div className="category-card" onClick={() => handleCardClick('cloth')}>👕 Cloth</div>
          <div className="category-card" onClick={() => handleCardClick('accessory')}>⌚ Accessory</div>
        </div>
      </div>

      {/* LOGIN MODAL */}
      {loginModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content login-modal">
            <h3>Account Sign In</h3>
            <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div className="input-group">
                <input type="text" required className="auth-input-full" value={inputUsername} onChange={(e) => setInputUsername(e.target.value)} />
                <label className="floating-label">Username</label>
              </div>
              <div className="input-group">
                <input type="password" required className="auth-input-full" value={inputPassword} onChange={(e) => setInputPassword(e.target.value)} />
                <label className="floating-label">Password</label>
              </div>
              <button type="submit" className="btn btn-login form-submit-btn" disabled={isLoggingIn}>
                {isLoggingIn ? "Processing..." : "Sign In"}
              </button>
              <button type="button" className="btn close-btn" onClick={() => setLoginModalOpen(false)}>Cancel</button>
            </form>
          </div>
        </div>
      )}

      {/* PRODUCTS DISPLAY MODAL */}
      {modalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Available {selectedCategory.toUpperCase()} Items</h3>
            <p style={{fontSize: "0.85rem", color: "#666"}}>*Multiple rows select kar sakte hain. Selected items par button RED ho jayega.</p>
            
            <div style={{ margin: '20px 0' }}>
              {products.map((item) => {
                const isSelected = selectedItemIds.includes(item.id);
                return (
                  <div 
                    key={item.id} 
                    className={`modal-item ${isSelected ? 'selected' : ''}`}
                    onClick={() => toggleItemSelection(item.id)}
                  >
                    <span style={{fontWeight: '500'}}>{item.name}</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                      <span>₹{item.base_price}</span>
                      <button className={`add-btn ${isSelected ? 'red' : ''}`} type="button">
                        {isSelected ? "Selected" : "Add+"}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            <button 
              className="btn btn-login" 
              style={{width: '100%', padding: '12px', background: '#2e7d32'}}
              onClick={handleBulkCheckout}
              disabled={isProcessingCart || selectedItemIds.length === 0}
            >
              {isProcessingCart ? "Calculating Sum..." : `Calculate Sum & Apply ${selectedItemIds.length * 5}% Cut`}
            </button>

            {/* LIVE DATA SYNC LOG FROM MYSQL TABLE */}
            {backendResponse && (
              <div className="db-response-box fade-in-effect">
                <p style={{ color: '#1b5e20', fontWeight: 'bold' }}>✓ {backendResponse.message}</p>
                <p>Gross Base Sum: <b>₹{backendResponse.total_base_sum}</b></p>
                <p>Cumulative Cut: <b style={{color: '#d32f2f'}}>-{backendResponse.discount_percentage}</b></p>
                <p>Saved Discount Cash: <b>₹{backendResponse.discount_amount}</b></p>
                <hr style={{borderColor: '#a5d6a7'}} />
                <p style={{fontSize: '1.15rem'}}>Net Payable Saved DB: <b>₹{backendResponse.final_payable_amount}</b></p>
              </div>
            )}

            <button className="btn close-btn" onClick={() => setModalOpen(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;