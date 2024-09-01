import {useEffect} from "react";
import {useAppContext} from "../contexts/AppContext.tsx";
import PromptToolbar from "../components/PromptToolbar.tsx";
import ImageGallery from "../components/ImageGallery.tsx";

export default function ImageGenerationPage() {
    const {userImagesList, setUserImagesList} = useAppContext()

    useEffect(() => {

        fetch(import.meta.env.VITE_API_BASE_URL + '/api/images/user/123')
            .then(response => response.json())
            .then(data => {
                setUserImagesList(data);
            });
    }, []);


    return (
        <div
            className="m-5 divide-y divide-gray-200 overflow-hidden rounded-lg bg-white shadow border-2 border-gray-200">
            <div className="px-4 py-5 sm:px-6">
                <PromptToolbar></PromptToolbar>

            </div>
            <div className="px-4 py-5 sm:p-6">

                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <ImageGallery userImages={userImagesList}>
                    </ImageGallery>


                </div>


            </div>
        </div>
    )
}