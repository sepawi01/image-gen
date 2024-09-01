import Header from "./components/Header.tsx";

import {AppProvider} from "./contexts/AppContext.tsx";
import ImageGenerationPage from "./pages/ImageGeneration.tsx";


function App() {

    return (
        <>
            <AppProvider>
                <Header
                    logo={"https://parksandresorts.com/assets/themes/parksandresorts/resources/images/par_logo.svg"}
                    title={"AI Image Studio"}
                ></Header>

                <ImageGenerationPage></ImageGenerationPage>
            </AppProvider>
        </>
    )
}

export default App
