import Header from "./Header.tsx";
import PromptBoard from "./PromptBoard/PromptBoard.tsx";
import {PromptProvider} from "../contexts/PromptContext.tsx";


function App() {

    return (
        <>
            <PromptProvider>
                <Header
                    logo={"https://parksandresorts.com/assets/themes/parksandresorts/resources/images/par_logo.svg"}
                    title={"AI Image Studio"}
                ></Header>

                <PromptBoard></PromptBoard>
            </PromptProvider>
        </>
    )
}

export default App
