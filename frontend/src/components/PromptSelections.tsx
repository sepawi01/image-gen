import {useAppContext} from "../contexts/AppContext.tsx";


export default function PromptSelections() {
    const {quality, setQuality, size, setSize, style, setStyle} = useAppContext()

    return (
        <div className="flex space-x-4 mb-4">
            <div>
                <label htmlFor="quality" className="block text-sm font-medium leading-6 text-gray-900">
                    Kvalité
                </label>
                <select
                    id="quality"
                    name="quality"
                    value={quality}
                    onChange={(e) => setQuality(e.target.value)}
                    className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
                >
                    <option value="standard">Standard</option>
                    <option value="hd">HD</option>
                </select>
            </div>

            <div>
                <label htmlFor="size" className="block text-sm font-medium leading-6 text-gray-900">
                    Storlek
                </label>
                <select
                    id="size"
                    name="size"
                    value={size}
                    onChange={(e) => setSize(e.target.value)}
                    className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
                >
                    <option value="1024x1024">1024x1024</option>
                    <option value="1792x1024">1792x1024</option>
                    <option value="1024x1792">1024x1792</option>
                </select>
            </div>

            <div>
                <label htmlFor="style" className="block text-sm font-medium leading-6 text-gray-900">
                    Stil
                </label>
                <select
                    id="style"
                    name="style"
                    value={style}
                    onChange={(e) => setStyle(e.target.value)}
                    className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
                >
                    <option value="vivid">Vivid</option>
                    <option value="natural">Natural</option>
                </select>
            </div>
        </div>
    );
}
