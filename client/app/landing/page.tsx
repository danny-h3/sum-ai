import { InputWithButton } from "./input-with-button";

export default function LandingPage() { 
    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <div className="text-5xl font-semibold text-center text-neutral-700 mb-6">
                <p> What&apos;s up? </p>
            </div>

            <div className="w-full max-w-2xl">
                <InputWithButton></InputWithButton>
            </div>
        </div>
    );
}