
export const handlePressMenu = (menuOpen, setMenuOpen) => () =>{
    setMenuOpen(!menuOpen);
}

export const countInputWord = (setWordCount) => (event) =>{
    const text = event.target.value;
    //console.log(text.length)
    setWordCount(text.length)
}

// export const handleLogout = () => {
//     setUser(null);
//     sessionStorage.removeItem("user");
//     navigate("/login");
// };